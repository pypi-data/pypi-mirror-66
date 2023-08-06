"""Credit to Kyle Piper (@krayzpipes - https://github.com/krayzpipes)
    This project was started by swiping, with permission, code Kyle wrote for ACE located here: https://github.com/ace-ecosystem/ACE/lib/saq/graph_api.py
"""

import os
import msal
import glob
import atexit
import logging
import requests
import urllib.parse
import configparser

from msgapi.config import DEFAULT_RESOURCE_CONFIGURATION_DIR_PATHS, TOKEN_CACHE


OVERVIEW = 'overview'
ARGUMENTS = 'arguments'
RESOURCE = 'resource'
ARGUMENT_HELP = 'argument_help'
REQUIRED_RESOURCE_SECTIONS = [OVERVIEW, ARGUMENTS, RESOURCE]
SECTION_ARGUMENTS = {'required': [],
                      'optional': ['required', 'optional']}
SECTION_OVERVIEW = {'required': ['name', 'description'],
                     'optional': []}
SECTION_RESOURCE = {'required': ['version', 'resource'],
                     'optional': ['parameters']}   


def validate_resource_configuation(resource_config):
    """Validate a resource configuration file.
    """
    if not all(rrs in resource_config.sections() for rrs in REQUIRED_RESOURCE_SECTIONS):
        logging.error(f"Resource configuration is missing required sections.")
        return False
    overview = resource_config[OVERVIEW]
    for _k in SECTION_OVERVIEW['required']:
        if overview.get(_k, None) is None:
            logging.error(f"Missing '{_k}' value in {OVERVIEW} section for resource config.")
            return False
    resource = resource_config[RESOURCE]
    for _k in SECTION_RESOURCE['required']:
        if resource.get(_k, None) is None:
            logging.error(f"Missing '{_k}' value in {RESOURCE} section for resource config.")
            return False
    args = resource_config[ARGUMENTS]
    for _k in SECTION_ARGUMENTS['required']:
        if args.get(_k, None) is None:
            logging.error(f"Missing '{_k}' value in {ARGUMENTS} section for resource config.")
            return False
    # Additional step for arguments, make sure default is configured for and defined optional arguments
    optional_args = args['optional'] if 'optional' in args else None
    if optional_args:
        for arg in optional_args.split(','):
            if args.get(arg, None) is None:
                logging.error(f"Missing default value for optional argument '{arg}' specified in {ARGUMENTS}->optional of resource config.")
                return False
    return True


def load_resources(resource_dirs=DEFAULT_RESOURCE_CONFIGURATION_DIR_PATHS):
    """Load defined MS Graph API resources from configuration files.

    :return: list of msgapi.Resource
    """
    resources = []
    for resource_dir in resource_dirs:
        for rc_path in glob.glob(f"{resource_dir}/*.ini"):
            logging.debug(f"Loading {rc_path}")
            resource_config = configparser.ConfigParser()
            resource_config.read(rc_path)
            if not validate_resource_configuation(resource_config):
                continue
            try:
                name = resource_config[OVERVIEW]['name']
                desc = resource_config[OVERVIEW]['description']
                version = resource_config[RESOURCE]['version']
                resource = resource_config[RESOURCE]['resource']
                parameter_string = resource_config[RESOURCE]['parameters'] if 'parameters' in resource_config[RESOURCE] else None
                args = {'required': {},
                        'optional': {},
                        'descriptions': {}}
                argument_descriptions = {}
                if ARGUMENT_HELP in resource_config.sections():
                    argument_descriptions = resource_config[ARGUMENT_HELP]
                optional_args = resource_config[ARGUMENTS].get('optional', None)
                if optional_args:
                    optional_args = resource_config[ARGUMENTS]['optional'].split(',')
                    for arg in optional_args:
                        args['optional'][arg] = resource_config[ARGUMENTS][arg]
                        #if argument_descriptions is not None:
                        args['descriptions'][arg] = argument_descriptions.get(arg, None)
                required_args = resource_config[ARGUMENTS].get('required', None)
                if required_args:
                    required_args = resource_config[ARGUMENTS]['required'].split(',')
                    for arg in required_args:
                        args['required'][arg] = None
                        #if argument_descriptions is not None:
                        args['descriptions'][arg] = argument_descriptions.get(arg, None)
                resources.append(Resource(version, resource, name, desc, parameter_string, args))
            except Exception as e:
                logging.error(f"Problem parsing resource config at {rc_path} : {e}")
                continue
    return resources


class Resource:
    """Represents a MS Graph API REST Resource
    """

    def __init__(self, version, resource_endpoint, name, description, parameter_str, args, **kwargs):
        self.api_version = version
        self.resource = resource_endpoint
        self.name = name
        self.description = description
        self.parameter_str = parameter_str
        self.args = args
        for key, value in kwargs.items():
            if key in self.args['required'].keys():
                self.args['required'][key] = value
            elif key in self.args['optional'].keys():
                self.args['optional'][key] = value

    def set_argument(self, key, value):
        if key in self.args['required'].keys():
            self.args['required'][key] = value
            return True
        elif key in self.args['optional'].keys():
            self.args['optional'][key] = value
            return True
        else:
            logging.warning(f"{key} is not a defined argument for this resource.")
            return False

    @property
    def ready(self):
        for key in self.args['required'].keys():
            if self.args['required'][key] is None:
                return False
        return True

    def __str__(self):
        txt = "\nMS Graph API Resource Configuration:\n"
        txt += "-----------------------------------\n"
        txt += "\t"+u'\u21B3' + f" Name: {self.name}\n"
        txt += "\t"+u'\u21B3' + f" Description: {self.description}\n"
        txt += "\t"+u'\u21B3' + f" API Version: {self.api_version}\n"
        txt += "\t"+u'\u21B3' + f" API Resource: {self.resource}\n"
        txt += "\t"+u'\u21B3' + f" Parameter String: {self.parameter_str}\n"
        txt += "\t"+u'\u21B3' + f" Arguments: \n"
        txt += "\t\t"+u'\u21B3' + f" Required: {self.args['required']}\n"
        txt += "\t\t"+u'\u21B3' + f" Optional Defaults: {self.args['optional']}\n"
        txt += "\t\t"+u'\u21B3' + f" Descriptions: {self.args['descriptions']}\n"
        return txt


def read_private_key(key_path, **kwargs):
    """Helper function to return private key read from .pem file."""

    _open = kwargs.get('opener') or open  # For testing with StringIO or BytesIO

    if not os.path.exists(key_path):
        return None
    with _open(key_path) as kf:
        return kf.read() 


class GraphConfig:
    """Helper class to abstract Graph API Config setup."""

    def __init__(self, section: configparser.SectionProxy, **kwargs):
        self.client_id = section["client_id"]
        self.authority = urllib.parse.urljoin(section['authority_base_url'], section['tenant_id'])
        self.scopes = section["scopes"].split(',')
        self.thumbprint = section["thumbprint"]
        self.private_key = kwargs.get('private_key') or read_private_key(section["private_key_file"])
        self.endpoint = section["endpoint"]
        self.client_credential = section.get("client_credential", None)
        if self.client_credential is None:
            self.client_credential = {
                "thumbprint": self.thumbprint,
                "private_key": self.private_key
            }

    @property
    def auth_kwargs(self):
        """Return dictionary of required kwargs when setting up the app."""

        return {
            "authority": self.authority,
            "client_credential": self.client_credential,
        }


CACHE = msal.SerializableTokenCache()
if TOKEN_CACHE and os.path.exists(TOKEN_CACHE):
    CACHE.deserialize(open(TOKEN_CACHE, "r").read())
if TOKEN_CACHE is not None:
    atexit.register(lambda:
        open(TOKEN_CACHE, "w").write(CACHE.serialize())
        # Hint: The following optional line persists only when state changed
        if CACHE.has_state_changed else None
        )

class GraphAPI:
    """API for making authenticated GraphAPI requests.

    Graph config requires the following format:

    graph_config = {
        'client_id' : 'whatever-uuid',
        'authority_base_url': 'https://whatever',
        'tenant_id': 'whatever-uuid',
        'scopes': 'comma-separated-string-of-scopes',
        'thumbprint': 'thumbprint associated with the key',
        'private_key_file': 'path to the private key file',
        'endpoint': 'the graph API base endpoint',
    }
    """

    def __init__(self, graph_config, verify_auth=True, verify_graph=True, proxies=None, **kwargs):
        self.config = kwargs.get('config_override')
        if not self.config:
            if not isinstance(graph_config, configparser.SectionProxy):
                if not isinstance(graph_config, configparser.ConfigParser):
                    raise TypeError(f"graph_config of type {type(graph_config)} not supported")
                else:
                    # assume 'default' section
                    graph_config = graph_config['default']
            self.config = GraphConfig(graph_config)
        self.proxies = proxies or {}
        self.client_app = None
        self.token = None
        self.verify = verify_graph
        self.verify_auth = verify_auth
        self.base_url = self.config.endpoint
        resource_dirs = kwargs.get('resource_dirs') or DEFAULT_RESOURCE_CONFIGURATION_DIR_PATHS
        self._resources = load_resources(resource_dirs=resource_dirs)
        self._resource_map = {}
        for _r in self._resources:
            self._resource_map[_r.name] = _r

    def initialize(self, **kwargs):
        """By having this function, you can configure your GraphAPI without
        kicking off the I/O of setting up a client app until you're ready
        to initialize it."""
        self.client_app = kwargs.get('client_app') or msal.ConfidentialClientApplication(
            self.config.client_id, **self.config.auth_kwargs, verify=self.verify_auth, timeout=5, proxies=self.proxies, token_cache=CACHE,
        )

    def build_url(self, path):
        return urllib.parse.urljoin(self.base_url, path)

    def get_token(self, **kwargs):
        logging.info("getting azure ad token from cache")
        if not self.client_app:
            self.initialize()
        result = self.client_app.acquire_token_silent(self.config.scopes, account=None)

        if not result:
            logging.info("token not found in cache: will attempt to acquire new token from azure ad")
            result = self.client_app.acquire_token_for_client(self.config.scopes)

        if 'access_token' not in result:
            logging.error(f"{result.get('error')}")
        self.token = result

    def request(self, endpoint, *args, method='get', proxies=None, **kwargs):
        """Return Graph API result after injecting the token into the request."""

        logging.debug(f'entering GraphAPI.request() with endpoint {endpoint}')

        _proxies = proxies or self.proxies

        # TODO - Do we need a 'refresh' process in case the token expires after 1 hour?
        if not self.token:
            self.get_token()

        # If the endpoint is not defined properly in the configuration, then it can cause the
        # urllib.parse.urljoin in self.build_url to join paths incorrectly.
        if self.base_url not in endpoint:
            logging.error(
                f"endpoint {endpoint} does not contain base url {self.base_url}--verify the url path is "
                f"joined to the base url correctly"
            )
            raise ValueError("graph api base_url missing from request")

        request_method = kwargs.get('request_method') or getattr(requests, method, None)

        if request_method is None:
            logging.error("method passed to graph api is not valid for requests library")

        http_headers = {
            'Authorization': f"Bearer {self.token['access_token']}",
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        if kwargs.get('headers'):
            http_headers = {**http_headers, **kwargs['headers']}

        logging.info(f'making authenticated graph api request HTTP {method.upper()} {endpoint}')
        return request_method(endpoint, *args, headers=http_headers, verify=self.verify, proxies=_proxies, **kwargs)

    @property
    def resource_names(self):
        return [r.name for r in self._resources]

    def get_resource(self, resource: str):
        """Get a previously configured MS Graph API REST resource.

        :param str resource: The name of the resource
        :return: msgapi.Resource
        """
        if resource not in self.resource_names:
            logging.info(f"No loaded resource by the name '{resource}'")
            return None
        return self._resource_map[resource]

    def execute_resource(self, resource: Resource, **kwargs):
        """Execute the MS Graph API REST resource, as configured.
        """
        for key, value in kwargs.items():
            resource.set_argument(key, value)
        if not resource.ready:
            logging.warning(f"Resource '{resource.name}' is missing required arguments.")
            return False
        
        url_path = f"{resource.api_version}/{resource.resource}"
        if resource.parameter_str is not None:
            _all_arguments = resource.args['required']
            _all_arguments.update(resource.args['optional'])
            resource.parameter_str = resource.parameter_str.format(**_all_arguments)
            url_path += f"{resource.parameter_str}"
        url = self.build_url(url_path)
        response = self.request(url)
        if response.status_code != 200:
            error = response.json()['error']
            logging.error(f"HTTP Status Code {response.status_code} : {error['code']} : {error['message']}")
        return response.json()
