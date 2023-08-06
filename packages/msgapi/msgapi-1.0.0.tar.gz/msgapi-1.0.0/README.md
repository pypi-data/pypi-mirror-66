# msgapi : Microsoft GraphAPI library

A python library and tool for interfacing with [Microsoft's Graph API](https://developer.microsoft.com/en-us/graph).

## Install

`pip install msgapi`

## Configure

There is an example graph config file supplied with some defaults at `msgapi/etc/graph_config.ini `. You can fill in your GraphAPI details directly or copy that file and complete it. The `msgapi.config.GRAPH_CONFIG` object (and the cli tool) will load configurations along the following paths:

```python3
GRAPH_CONFIG_TEMPLATE = os.path.join(HOME_PATH, ETC_DIR, 'graph_config.ini')
GLOBAL_GRAPH_CONFIG = '/etc/msgraph/graph_config.ini'
USER_GRAPH_CONFIG = os.path.join(os.path.expanduser("~"),'.config', 'msgapi', 'graph_config.ini')
# Later configs override earlier configs
DEFAULT_GRAPH_CONFIGS = [GRAPH_CONFIG_TEMPLATE, GLOBAL_GRAPH_CONFIG, USER_GRAPH_CONFIG]
```

You can also supply your configurations to the msgapi.GraphAPI object like so:

```python3
graph_config = msgapi.config.load_config(['/your/config/path'])
client_app = msgapi.GraphAPI(graph_config)
```


## On the CLI it's "msgraphi"

A CLI tool is included named `msgraphi`. The tool was written to take advantage of "resource configurations" to allow for quick and dynamic evaluation/use of the stupid number of MS graph rest resources that are available for consumption. These resource configurations are dynamically added to msgraphi as cli arguments. See the resource configuration section for more details.

There are also some built in methods available via the cli tool that are defined in the `functions.py`. Such as `scramble-password` and some `email` related functionality.

Also, a `-raw` request resource available on the cli that allows you to pass resoure requests directly to the GraphAPI client request method.

## Resource Configurations

There were so many ms graph api resources to test for various things I made a resource config parser so I could evaluate resources quickly and save them for future use. This way code doesn't have to be written to test things or for data carving on the command line.

### There is a template

There is a template with some more explainations for how these fields are parsed and evaluated at `msgapi/etc/resource_configuration_template.ini`:

```
[overview]
; The name you want to give this resource, usually something very similar to the REST resource name itself
name=
; A description of the resource, perhaps with link to MS documentation too
description=

# Use the arguments section to define any required or optional arguments you
# want to pass to the REST resource as parameters
[arguments]
; comma seperated list of required arguments that MUST be supplied to the resource at run time
required=
; comma seperated list of optional arguments that can be overridden, but MUST have defaults defined
optional=
; example optional:
#optional=riskState,riskLevel
; Then you'd have to have a riskState and riskLevel key in this section, with a value defined for each, like so:
#riskState=atRisk
#riskLevel=high

# The argument_help section should contain helpful descriptions of arguments defined in the arguments section
[argument_help]
; example
#riskLastUpdatedDateTime=The date and time that the risky user was last updated. Ex: 2020-03-19T00:00:00.000Z

# The resource section describes the MS Graph API resource and how to query it. The parameters key is not required.
[resource]
; The MS Graph API version. (required) example: beta or v1.0 
version=
; The location of the resource. (required) example: riskyUsers or 'security/alerts'
resource=
; The format of how you would like to pass any parameters to this resource
; note that you have to include the '/' or '?$' depending on your needs
parameters=
; example:
#parameters=?$filter=riskLevel eq microsoft.graph.riskLevel'{riskLevel}' and riskState eq microsoft.graph.riskState'{riskState}' and riskLastUpdatedDateTime gt {riskLastUpdatedDateTime}
```

### Example resource config 

Showing `msgapi/resource_configurations/riskyUsers.ini`:
```
[overview]
name=riskyUsers
description=List risky users and their properties. (https://docs.microsoft.com/en-us/graph/api/resources/riskyuser?view=graph-rest-beta)

[arguments]
required=riskLastUpdatedDateTime
optional=riskState,riskLevel
# optinal argument defauls
riskState=atRisk
riskLevel=high

[argument_help]
riskLastUpdatedDateTime=The date and time that the risky user was last updated. Ex: 2020-03-19T00:00:00.000Z
riskState=possible values are confirmedSafe, remediated, atRisk, unknownFutureValue
riskLevel=possible values are low, medium, high, hidden

[resource]
version=beta
resource=riskyUsers
parameters=?$filter=riskLevel eq microsoft.graph.riskLevel'{riskLevel}' and riskState eq microsoft.graph.riskState'{riskState}' and riskLastUpdatedDateTime gt {riskLastUpdatedDateTime}
```

##### There are several resource configurations included:

```bash
$ grep -r msgapi/resource_configurations/ -e name
msgapi/resource_configurations/get_user.ini:name=get_user
msgapi/resource_configurations/riskyUsers.ini:name=riskyUsers
msgapi/resource_configurations/get_security_alert.ini:name=get_security_alert
msgapi/resource_configurations/list_signIns.ini:name=List_Sign-Ins
msgapi/resource_configurations/list_security_alerts.ini:name=list_security_alerts
msgapi/resource_configurations/get_secureScore.ini:name=get_secureScore
msgapi/resource_configurations/history_of_riskyUser.ini:name=history_of_riskyUser
msgapi/resource_configurations/list_secureScores.ini:name=list_secureScores
```

## Credit

Thanks to [Kyle Piper](https://github.com/krayzpipes) for writing the initial GraphAPI and GraphConfig classes. This library was started by swiping those classes from the code Kyle wrote for ACE located here: [https://github.com/ace-ecosystem/ACE/lib/saq/graph_api.py](https://github.com/ace-ecosystem/ACE/lib/saq/graph_api.py). There are also several functions in this projects `functions.py` that were written by Kyle 👏.
