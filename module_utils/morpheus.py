#!/usr/bin/python
import requests
import os
import json
from ansible.module_utils.basic import AnsibleModule
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def morph_argspec():
    argument_spec = dict(
        baseurlurl = dict(required=False, default=os.environ.get('MORPH_ADDR', ''), type='str'),
        authtype = dict(required=False, default=os.environ.get('MORPH_AUTHTYPE', 'token'), type='str'),
        api_token = dict(required=False, default=morphtoken(), type='str', no_log=True),
        username = dict(required=False, default=os.environ.get('MORPH_USER', ''), type='str'),
        password = dict(required=False, default=os.environ.get('MORPH_PASSWORD', ''), type='str', no_log=True)
    )
    return argument_spec

def morph_init(argument_spec, supports_check_mode=False):
    return AnsibleModule(argument_spec=argument_spec, supports_check_mode=supports_check_mode)

def morphtoken():
    if 'MORPH_TOKEN' in os.environ:
        return os.environ['MORPH_TOKEN']
    token_file = os.path.expanduser('~/.morphtoken')
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return f.read().strip()
    else:
        username = os.environ['MORPH_USER']
        password = os.environ['MORPH_PASSWORD']
        url = urljoin(os.environ['MORPH_ADDR'], 'oauth')
        access = {
            "grant_type": "password",
            "scope": "write",
            "client_id": "morph-customer"
            }
        url2 = url + '/token?%s' % urlencode(access)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-agent': 'curl/7.51.0'
        }
        res = requests.post(url2, data=payload, headers=headers)
        json_response = json.loads(res.text)
        return json_response["access_token"]   
    return ''

def morphwrapper(function):
    def wrapper(*args, **kwargs):
        result = { "changed": False, "rc" : 0}
        try:
            result.update(function(*args, **kwargs))
        except Exception as e:
            result['rc'] = 1
            result['failed'] = True
            result['msg'] = u"Exception: " + str(e)
        return result
    return wrapper


