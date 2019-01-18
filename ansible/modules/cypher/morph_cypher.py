#!/usr/bin/python
import requests
import json
import posixpath
from ansible.module_utils.basic import *
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def morph_auth(module):

    url = urljoin(module.params["baseurl"], 'oauth')
    access = {
        "grant_type": "password",
        "scope": "write",
        "client_id": "morph-customer"
    }

    url2 = url + '/token?%s' % urlencode(access)
    payload = "username=" + module.params["username"] + "&password=" + module.params["password"]
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-agent': 'curl/7.51.0'
    }
    res = requests.post(url2, data=payload, headers=headers)
    json_response = json.loads(res.text)
    access_token = json_response["access_token"]
    return access_token


def morph_secret(module):

    result = { "changed": False}

    cypher = posixpath.join('api', 'cypher')
    url = urljoin(module.params["baseurl"], cypher)
    headers = {"Authorization": "BEARER " + module.params["api_token"]}
    json_data = requests.get(url, headers=headers).json()
    match = next(d["id"] for d in json_data["cyphers"] if d["itemKey"] == module.params["secret_key"])
    
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