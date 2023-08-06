
import json
import logging
import configparser

from typing import Union

from msgapi import GraphAPI
from msgapi.config import RESULT_MESSAGE_NOT_FOUND, RESULT_MESSAGE_FOUND


def scramble_password(api: GraphAPI, id_or_upn: str, password: str, **kwargs):
    """
    https://docs.microsoft.com/en-us/graph/api/user-update?view=graph-rest-1.0&tabs=http
    https://docs.microsoft.com/answers/questions/9024/error-while-updating-the-password-profile.html
    """
    data = {"passwordProfile": {
                "forceChangePasswordNextSignIn": True,
               "forceChangePasswordNextSignInWithMfa": False,
               "password": password }
             }
    url = api.build_url(f"v1.0/users/{id_or_upn}")
    response = api.request(url, data=json.dumps(data), method='patch')
    if response.status_code != 200:
        error = response.json()['error']
        logging.error(f"HTTP Status Code {response.status_code} : {error['code']} : {error['message']}")
    return response.json()

def list_security_alerts(api: GraphAPI, **kwargs):
    url = api.build_url("security/alerts")
    response = api.request(url)
    return response


def list_high_risk_users(api: GraphAPI, riskLastUpdatedDateTime=None):
    """
    Get Risky Users with a riskLevel of 'high'

    Parameters
    ----------
    api: GraphAPI
        A configured GraphAPI object, with token.
    """
    filter = "riskLevel eq microsoft.graph.riskLevel'high' and riskState eq microsoft.graph.riskState'atRisk'"
    if riskLastUpdatedDateTime:
        filter += f" and riskLastUpdatedDateTime gt {riskLastUpdatedDateTime}"
    url = api.build_url(f"beta/riskyUsers?$filter={filter}")
    response = api.request(url)
    if response.status_code != 200:
        error = response.json()['error']
        logging.error(f"HTTP Status Code {response.status_code} : {error['code']} : {error['message']}")
    return response.json()

def get_risky_user(api: GraphAPI, id: str, history=False):
    if history:
        url = api.build_url(f"beta/riskyUsers/{id}/history")
    else:
        url = api.build_url(f"beta/riskyUsers/{id}")
    response = api.request(url)
    if response.status_code != 200:
        error = response.json()['error']
        logging.error(f"HTTP Status Code {response.status_code} : {error['code']} : {error['message']}")
    return response.json()

def get_identity_risk_event(api: GraphAPI, id: str):
    url = api.build_url(f"beta/identityRiskEvents/{id}")
    response = api.request(url)
    if response.status_code != 200:
        error = response.json()['error']
        logging.error(f"HTTP Status Code {response.status_code} : {error['code']} : {error['message']}")
    return response.json()


def find_email_by_message_id(api: GraphAPI, user: str, message_id: str, folder: str = None, **kwargs) -> Union[None, str]:
    _request_func = kwargs.get('request_func') or api.request

    url = api.build_url(f"{user}/messages")
    if folder is not None:
        url = api.build_url(f"{user}/mailFolders/{folder}/messages")
    params = {'$filter': f"internetMessageId eq '{message_id}'"}
    response = _request_func(url, method='get', params=params, **kwargs)

    try:
        messages = response.json()['value']
    except KeyError:
        logging.info(f"could not find message id {message_id} at {url} for user {user}, folder {folder}, "
                     f"status_code: {response.status_code}, reason: '{response.reason}'")
        return None
    except AttributeError:
        logging.error(f"response did not have json attribute for message id {message_id} at {url} "
                      f"for user {user}, folder {folder}, status_code: {response.status_code}, reason: {response.reason}")
        return None
    else:
        if not messages:
            logging.info(f"no messages found for message id {message_id} at {url} for user {user} folder {folder}")
            return None

        _id = messages[0]['id']
        logging.debug(f"found message id {message_id} at {url} as o365 item {_id} for user {user} folder {folder}")
        return _id


def get_mime_content_by_o365_id(api, user, item_id, **kwargs):
    """Return the email mime content from Graph API."""

    _request_func = kwargs.get('request_func') or api.request

    url = api.build_url(f"{user}/messages/{item_id}/$value")
    # Turns out, you don't need this next piece to get deleted emails.
    # if folder is not None:
    #     url = api.build_url(f"{user}/mailFolder/{folder}/messages/{item_id}/$value")
    response = _request_func(url, method='get')
    if response.status_code != 200:
        return None, RESULT_MESSAGE_NOT_FOUND
    return response.text, RESULT_MESSAGE_FOUND


def move_mail(api: GraphAPI, user: str, item_id: str, destination: str, **kwargs) -> bool:
    _request_func = kwargs.get('request_func') or api.request
    _build_url = kwargs.get('build_url') or api.build_url

    url = _build_url(f'{user}/messages/{item_id}/move')
    _json = {'destinationId': destination}
    response = _request_func(url, method='post', json=_json)
    if response.status_code != 201:
        logging.warning(f'mail not moved for user {user}, item_id {item_id}, destination '
                        f'{destination}, status_code {response.status_code} reason {response.text}')
        return False
    logging.info(f'successfully moved mail for {user}, item_id {item_id}, destination'
                 f'{destination}')
    return True


def get_graph_api_object(config_section: configparser.SectionProxy, **kwargs) -> GraphAPI:
    _api_class = kwargs.get('api_class') or GraphAPI
    auth_ca_cert = config_section.get('auth_ca_cert_path', True)
    graph_ca_cert = config_section.get('graph_ca_cert_path', True)
    proxies = kwargs.get('proxies') or proxies()

    try:
        return _api_class(
            config_section,
            verify_auth=auth_ca_cert,
            verify_graph=graph_ca_cert,
            proxies=proxies,
        )
    except Exception as e:
        logging.error(f"error creating Graph API object: {e.__class__} '{e}'")
        raise e