#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys
import json
import logging
import argparse
import argcomplete
import coloredlogs

from msgapi.config import CONFIG, GRAPH_CONFIG, RESOURCE_CONFIG_TEMPLATE
from msgapi import GraphAPI, load_resources
from msgapi.functions import *

# configure logging #
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s')

logger = logging.getLogger()
coloredlogs.install(level='INFO', logger=logger)


def build_resource_parser(resource_subparsers, resources):
    """Parse pre-configured MS Graph API REST resources and add each to the given ArgumentParser.
    """
    for resource in resources:
        resource_parser = resource_subparsers.add_parser(resource.name, help=resource.description)
        for arg in resource.args['required']:
            help = resource.args['descriptions'].get(arg, "No help description available.")
            resource_parser.add_argument(arg, action='store', help=help)
        for arg in resource.args['optional']:
            abrv = '-'+arg[0]
            if '-h' == abrv or abrv in resource_parser._option_string_actions:
                abrv = '-'+arg[:2]
            help = resource.args['descriptions'].get(arg, "No help description available.")
            resource_parser.add_argument(abrv, '--'+arg, action='store', default=resource.args['optional'][arg], help=help)
        
    return resource_subparsers


def main():

    resources = load_resources()
    parser = argparse.ArgumentParser(description="MS Graph API on the CLI")
    parser.add_argument('-d', '--debug', action='store_true', help="Turn on debug logging.")
    parser.add_argument('-raw', '--raw-request-resource', action='store', help="Get a MS Graph API resource request directly. Ex: msgraphi -r 'security/alerts'")
    parser.add_argument('-prt', '--print-resource-template', action='store_true', help="Write the template for configuring resources.")
    parser.add_argument('-lr', '--list-configured-resources', action='store_true', help="List all pre-configured MS Graph API REST resources available.")
    parser.add_argument('-gr', '--get-resource', choices=[r.name for r in resources], action='store', dest='resource_name', help="Execute a pre-configured resource request.")
 
    subparsers = parser.add_subparsers(dest='instruction')

    parser_pw = subparsers.add_parser('scramble-password', help="Re-set a user's password and force them to change it on next log in.")
    parser_pw.add_argument('id_or_upn', action='store', help="The ID of UPN of a user.")
    parser_pw.add_argument('password', action='store', help="The temporary password to assign the user.")

    parser_email = subparsers.add_parser('email', help="Perform email related actions.")
    parser_email.add_argument('email_address', action='store', help="The user's email address.")
    parser_email.add_argument('message_id', action='store', help="The message id to work with.")

    build_resource_parser(subparsers, resources)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.debug:
        coloredlogs.install(level='DEBUG', logger=logger)

    # DEFAULT set up
    client_app = GraphAPI(GRAPH_CONFIG)

    if args.print_resource_template:
        with open(RESOURCE_CONFIG_TEMPLATE, 'r') as fp:
            for line in fp.readlines():
                print(line.strip())
        return True

    if args.raw_request_resource:
        if 'beta' in args.raw_request_resource:
            url = client_app.build_url(f"{args.raw_request_resource}")
        else: # assume version 1.0 API
            url = client_app.build_url(f"/v1.0/{args.raw_request_resource}")
        response = client_app.request(url)
        if response.status_code != 200:
            error = response.json()['error']
            logging.error(f"HTTP Status Code {response.status_code} : {error['code']} : {error['message']}")
        results = response.json()
        results = results['value'] if 'value' in results else results
        print(json.dumps(results, indent=2, sort_keys=True))
        return True

    if args.list_configured_resources:
        for resource in resources:
            print(resource)
        return True

    if args.resource_name:
        resource = client_app.get_resource(args.resource_name)
        if not resource.ready:
            print("Supply required arguments:")
            for arg in resource.args['required']:
                value = input(f"Set {arg}: ")
                resource.set_argument(arg, value)
            print("Change optional arugments, if you want:")
            for arg in resource.args['optional']:
                default = resource.args['optional'][arg]
                value = input(f"Set {arg} [{default}]: ") or default
                resource.set_argument(arg, value)
        results = client_app.execute_resource(resource)
        print(json.dumps(results, indent=2, sort_keys=True))
    
    if args.instruction == 'email':
        retults = find_email_by_message_id(client_app, args.email_address, args.message_id)
        print(json.dumps(results, indent=2, sort_keys=True))
        return True
    
    if args.instruction == 'scramble-password':
        results = scramble_password(client_app, args.id_or_upn, args.password)
        print(json.dumps(results, indent=2, sort_keys=True))
        return True

    # Dynamic instructions
    if args.instruction:
        resource_args = {}
        for key in [key for key in vars(args).keys() if vars(args)[key] and key != 'instruction' and key != 'debug']:
            resource_args[key] = vars(args)[key]
        resource = client_app.get_resource(args.instruction)
        results = client_app.execute_resource(resource, **resource_args)
        print(json.dumps(results, indent=2, sort_keys=True))
        return True
