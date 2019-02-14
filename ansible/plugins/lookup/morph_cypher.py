#!/usr/bin/env python
#
# Morph_Cypher Lookup Plugin
#
# A simple example of using the morph_cypher plugin in a role:
#    ---
#    - debug: msg="{{lookup('morph', 'ldapadmin', 'password')}}"
#
# The plugin must be run with MORPH_ADDR and MORPH_TOKEN set and
# exported.
#
# The plugin can be run manually for testing:
#     python ansible/plugins/lookup/morph_cypher.py ldapadmin password
#

import json
import os
import requests
import sys
import warnings
import posixpath

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.morpheus import (
    morph_auth,
    morph_get_client,
    morphtoken
)


class LookupModule(LookupBase):

    def _get_params(self, params):
        authtype = params['authtype']
        if authtype == 'userpass':
            if 'username' not in params:
                params['username'] = os.environ.get('MORPH_USER')
            if 'password' not in params:
                params['password'] = os.environ.get('MORPH_PASSWORD')
            params['api_token'] = morph_auth(params)
        else:
            if 'api_token' not in params:
                params['api_token'] = morphtoken()
        if 'baseurl' not in params:
            params['baseurl'] = os.environ.get('MORPH_ADDR')
        if 'ssl_verify' not in params:
            params['ssl_verify'] = os.environ.get('MORPH_SSL_VERIFY')
        if 'secret_key' not in params:
            params['secret_key'] = os.environ.get('MORPH_SECRET')
        return params


    def run(self, terms, variables=None, **kwargs):
        cypher_args = terms[0].split()
        params = {}
        ret = []

        for item in cypher_args:
            try:
                key, value = item.split('=')
            except ValueError:
                raise AnsibleError("morph_cypher lookup plugin needs ke=value pairs, but received %s" %terms)
            params[key] = value

        cypher = posixpath.join('api', 'cypher')
        client = morph_get_client(self._get_params(params), cypher)
        url = urljoin(params['baseurl'], cypher)
        headers = {'Authorization': 'BEARER ' + params['api_token']}
        match = [d['id'] for d in client['cyphers']][0]
        new_cypher = posixpath.join('cypher', str(match), 'decrypt')
        secret_url = urljoin(url, new_cypher)
        new_resp = requests.get(secret_url, headers=headers, verify=params['ssl_verify'])
        ret.append(new_resp.json()['cypher']['itemValue'])
        return ret
        
'''
def main(argv=sys.argv[1:]):
    if len(argv) < 1:
        print("Usage: morph_cypher.py path [key]")
        return -1
    params = {}
    for i in argv:
        key, value = [j.strip() for j in i.split('=', 1)]
        params[key] = value
    print(LookupModule().run(params))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''