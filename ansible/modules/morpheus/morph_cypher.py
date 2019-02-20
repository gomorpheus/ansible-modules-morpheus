#!/usr/bin/python
import requests
import json
import os
import posixpath
from ansible.module_utils.morpheus import (
    morph_get_client,
    morph_argspec,
    morph_init, 
    morphwrapper
)
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


ANSIBLE_METADATA = {'status': ['stableinterface'], 'supported_by': 'community', 'version': '0.0.2'}
DOCUMENTATION = '''
---
module: morph_cypher
version_added: "0.1.0"
short_description: Morpheus Cypher read module
description:
    - Module to read from Morpheus Cypher service.
options:
    baseurl:
        description:
            - url for Morpheus
        default:
            - to environment variable MORPH_ADDR
    authtype:
        description:
            - Defines how module builds client to Morpheus, through credentials or token
        default:
            - to environment variable MORPH_AUTHTYPE as token
    api_token:
        description:
            - API Token for Morpheus
        default:
            - to environment variable MORPH_TOKEN
    username:
        description:
            - Morpheus Username for userpass based auth
        default:
            - to environment variable MORPH_USER
    password:
        description:
            - Morpheus Password for userpass based auth
        default:
            - to environment variable MORPH_PASSWORD
    secret_key:
        description:
            - Secret key to read value from Morpheus
        default:
            - to environment variable MORPH_SECRET
    ssl_verify:
        description:
            - ignore ssl true or false
        default:
            - defaults to ssl_verify = True
    register:
        description:
            - variable to register result.
'''


@morphwrapper
def morph_secret(params):

    result = { "changed": False, "rc": 0}
    cypher = posixpath.join('api', 'cypher')
    query = {'itemKey': params['secret_key']}
    client = morph_get_client(params, cypher, query)
    #json_data = requests.get(url, headers=headers).json()
    
    if len(client['cyphers']) == 0:
        new_query = {'cypher': query}
        new_client = morph_post_client(self._get_params(params), cypher, new_query)
        match = new_client['cypher']['id']
    else:
        match = [d['id'] for d in client['cyphers']][0]

    url = urljoin(params["baseurl"], cypher)
    headers = {"Authorization": "BEARER " + params["api_token"]}
    new_cypher = posixpath.join('cypher', str(match), 'decrypt')
    secret_url = urljoin(url, new_cypher)
    new_resp = requests.get(secret_url, headers=headers, verify=params['ssl_verify'])
    #new_resp = morph_get_client(params, new_cypher)
    #result['secret'] = new_resp["cypher"]["itemValue"]
    result['secret'] = new_resp.json()["cypher"]["itemValue"]

    return result


def main():

    fields = morph_argspec()
    fields['secret_key'] = dict(required=True, default=os.environ.get('MORPH_SECRET'), type='str')

    module = morph_init(fields)
    
    result = morph_secret(module.params)

    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__=="__main__":
    main()