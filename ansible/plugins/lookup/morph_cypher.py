from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
      lookup: morph_cypher
        author: Adam Hicks <ahicks@morpheusdata.com>
        version_added: "0.1.0"
        short_description: read secrets from Morpheus's Cypher Vault
        description:
            - read secrets from Morpheus's Cypher Vault
        options:
          baseurl:
            description: URL for Morpheus
            required: True
          authtype:
            description: userpass based auth or token based auth
            required: True
          secret_key:
            description: The secret key to be read from Morpheus
            required: True
          username:
            description: Username for authenticating against Morpheus
            required: False
          password:
            description: password for Username for authenticating against Morpheus
            required: False
          api_token:
            description: Morpheus API Token for authenticating against Morpheus
            required: False
          ssl_verify:
            description: Ignore SSL warnings True or False
            required: False
        notes:
          - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
          - this lookup does not understand globing --- use the fileglob lookup instead.
"""

EXAMPLES = """
- debug:
    msg: "{{ lookup('morph_cypher', 'baseurl=https://sandbox.morpheusdata.com authtype=token api_token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx secret_key=password/spark')}}"

- debug:
    msg: "{{ lookup('morph_cypher', 'baseurl=https://sandbox.morpheusdata.com authtype=userpass username=slim_shady password=password secret_key=secret/hello') }}"

- debug:
    msg: "{{ lookup('morph_cypher', 'baseurl=https://sandbox.morpheusdata.com authtype=token api_token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx ssl_verify=False secret_key=key/256/myKey') }}"
"""

RETURN = """
_raw:
  description:
    - secrets(s) requested
"""

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
    morph_post_client,
    morphtoken
)
from ansible.utils.display import Display
display = Display()


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
                raise AnsibleError("morph_cypher lookup plugin needs key=value pairs, but received %s" %terms)
            params[key] = value
        
        query = {'itemKey': params['secret_key']}

        cypher = posixpath.join('api', 'cypher')
        client = morph_get_client(self._get_params(params), cypher, query)

        if len(client['cyphers']) == 0:
            new_query = {'cypher': query}
            new_client = morph_post_client(self._get_params(params), cypher, new_query)
            match = new_client['cypher']['id']
        else:
            match = [d['id'] for d in client['cyphers']][0]

        url = urljoin(params['baseurl'], cypher)
        headers = {'Authorization': 'BEARER ' + params['api_token']}
        new_cypher = posixpath.join('cypher', str(match), 'decrypt')
        secret_url = urljoin(url, new_cypher)
        new_resp = requests.get(secret_url, headers=headers, verify=params['ssl_verify'])
        ret.append(new_resp.json()['cypher']['itemValue'])
        return ret