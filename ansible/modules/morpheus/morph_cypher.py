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
def morph_secret(params):

    result = { "changed": False, "rc": 0}
    cypher = posixpath.join('api', 'cypher')
    client = morph_get_client(params, cypher)
    url = urljoin(params["baseurl"], cypher)
    headers = {"Authorization": "BEARER " + params["api_token"]}
    #json_data = requests.get(url, headers=headers).json()

    match = [d["id"] for d in client["cyphers"]][0]
    
    new_cypher = posixpath.join('cypher', str(match), 'decrypt')
    secret_url = urljoin(url, new_cypher)
    new_resp = requests.get(secret_url, headers=headers)
    #new_resp = morph_get_client(params, new_cypher)
    result['secret'] = new_resp.json()["cypher"]["itemValue"]

    return result


def main():

    fields = morph_argspec()
    fields['secret_key'] = dict(required=True, type='str')

    module = morph_init(fields)
    
    result = morph_secret(module.params)

    module.exit_json(**result)


if __name__=="__main__":
    main()