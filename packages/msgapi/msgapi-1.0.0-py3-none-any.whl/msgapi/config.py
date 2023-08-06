
import os
import json
import logging

from configparser import ConfigParser

# STATIC
RESULT_MAILBOX_NOT_FOUND = 'mailbox not found'
RESULT_MESSAGE_NOT_FOUND = 'message not found in folder'
RESULT_MESSAGE_FOUND = 'message found'

HOME_PATH = os.path.dirname(os.path.abspath(__file__))
ETC_DIR = os.path.join(HOME_PATH, 'etc')

# Connecting to MS Graph - NOTE: Either prompt for or use a secure key store to store your secrets, please
GRAPH_CONFIG_TEMPLATE = os.path.join(HOME_PATH, ETC_DIR, 'graph_config.ini')
GLOBAL_GRAPH_CONFIG = '/etc/msgraph/graph_config.ini'
USER_GRAPH_CONFIG = os.path.join(os.path.expanduser("~"),'.config', 'msgapi', 'graph_config.ini')
# Later configs override earlier configs
DEFAULT_GRAPH_CONFIGS = [GRAPH_CONFIG_TEMPLATE, GLOBAL_GRAPH_CONFIG, USER_GRAPH_CONFIG]

# MSGAPI configs define how this lib/tool works
DEFAULT_MSGAPI_CONFIG = os.path.join(HOME_PATH, ETC_DIR, 'msgapi_config.ini')
GLOBAL_MSGAPI_CONFIG_PATH = '/etc/msgraph/msgapi_config.ini'
USER_MSGAPI_CONFIG_PATH = os.path.join(os.path.expanduser("~"),'.config', 'msgapi', 'msgapi_config.ini')
# Later configs override earlier configs
DEFAULT_MSGAPI_CONFIG_PATHS = [DEFAULT_MSGAPI_CONFIG, GLOBAL_MSGAPI_CONFIG_PATH, USER_MSGAPI_CONFIG_PATH]

# Resource configurations
RESOURCE_CONFIG_TEMPLATE = os.path.join(HOME_PATH, ETC_DIR, 'resource_configuration_template.ini')
DEFAULT_RESOURCE_CONFIGURATIONS = os.path.join(HOME_PATH, 'resource_configurations')
GLOBAL_RESOURCE_CONFIGURATIONS = '/etc/msgraph/resource_configurations'
USER_RESOURCE_CONFIGURATIONS = os.path.join(os.path.expanduser("~"),'.config', 'msgapi', 'resource_configurations')
DEFAULT_RESOURCE_CONFIGURATION_DIR_PATHS = [DEFAULT_RESOURCE_CONFIGURATIONS, GLOBAL_RESOURCE_CONFIGURATIONS, USER_RESOURCE_CONFIGURATIONS]

TOKEN_CACHE = None
DEFAULT_TOKEN_CACHE = '/etc/msgraph/.token_cache.bin'
USER_TOKEN_CACHE =  os.path.join(os.path.expanduser("~"), '.cache', '.ipasm_token_cache.bin')
if os.access(os.path.dirname(DEFAULT_TOKEN_CACHE), os.W_OK):
    TOKEN_CACHE = DEFAULT_TOKEN_CACHE
elif os.access(os.path.dirname(USER_TOKEN_CACHE), os.W_OK):
    TOKEN_CACHE = USER_TOKEN_CACHE
else:
    logging.debug("No writtable path for saving a token cache.")

def load_config(config_paths, required_section=None, required_keys=[]):
    """Load MSGAPI or MS Graph configuration.

    :param list config_paths: List of configuration paths.
    :param list required: (optional) List of keys required to be in the config.
    """
    config = ConfigParser()
    finds = []
    for cp in config_paths:
        if os.path.exists(cp):
            logging.debug("Found config file at {}.".format(cp))
            finds.append(cp)
    if not finds:
        logging.critical("Didn't find any config files defined at these paths: {}".format(config_paths))
        raise Exception("MissingConfiguration", "Config paths : {}".format(config_paths))

    config.read(finds)
    
    return config

CONFIG = load_config(config_paths=DEFAULT_MSGAPI_CONFIG_PATHS)
GRAPH_CONFIG = load_config(config_paths=DEFAULT_GRAPH_CONFIGS)#, required_section='default', required_keys=['tenant_id', 'authority_base_url', 'client_id', 'scopes', 'endpoint'])
