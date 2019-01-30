#!/usr/bin/python
import requests
import json
import posixpath
from ansible.module_utils.basic import *
from ansible.module_utils.morpheus import *
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode



@morphwrapper
def morph_secret(module):

    result = { "changed": False, "rc": 0}

    cypher = posixpath.join('api', 'cypher')
    url = urljoin(module.params["baseurl"], cypher)
    headers = {"Authorization": "BEARER " + module.params["api_token"]}
    json_data = requests.get(url, headers=headers).json()

    match = [d["id"] for d in json_data["cyphers"]][0]
    
    new_cypher = posixpath.join('cypher', str(match), 'decrypt')
    secret_url = urljoin(url, new_cypher)
    new_resp = requests.get(secret_url, headers=headers)
    result['secret'] = new_resp.json()["cypher"]["itemValue"]

    return result


def main():

    fields = {
        "api_token": {"default": True, "type": "str"},
        "baseurl": {"default": True, "type": "str"},
        "secret_key": {"default": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    
    result = morph_secret(module)

    module.exit_json(**result)


if __name__=="__main__":
    main()