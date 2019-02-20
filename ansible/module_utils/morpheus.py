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
        baseurl = dict(required=False, default=os.environ.get('MORPH_ADDR', ''), type='str'),
        ssl_verify = dict(required=False, default=os.environ.get('MORPH_SSL_VERIFY', True), type='bool'),
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
    return ''


def morph_get_client(params, endpoint, query=None):
    verify = params.get('ssl_verify')
    authtype = params.get('authtype')
    baseurl = params.get('baseurl')
    if authtype == 'userpass':
        token = morph_auth(params)
    else:
        token = params.get('api_token')
    url = urljoin(baseurl, endpoint)
    headers = {"Authorization": "BEARER " + token}
    json_data = requests.get(url, headers=headers, params=query, verify=verify).json()
    return json_data

def morph_post_client(params, endpoint, query=None):
    verify = params.get('ssl_verify')
    authtype = params.get('authtype')
    baseurl = params.get('baseurl')
    if authtype == 'userpass':
        token = morph_auth(params)
    else:
        token = params.get('api_token')
    url = urljoin(baseurl, endpoint)
    headers = {"Authorization": "BEARER " + token}
    headers["Content-Type"] = "application/json"
    json_data = requests.post(url, headers=headers, json=query, verify=verify).json()
    return json_data

    

def morph_auth(params):
    username = params.get('username')
    password = params.get('password')
    baseurl = params.get('baseurl')
    url = urljoin(baseurl, 'oauth')
    access = {
        "grant_type": "password",
        "scope": "write",
        "client_id": "morph-customer"
        }
    url2 = url + '/token?{}'.format(urlencode(access))
    payload = "username=" + username + "&password=" + password
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-agent': 'curl/7.51.0'
        }
    res = requests.post(url2, data=payload, headers=headers)
    json_response = json.loads(res.text)
    return json_response["access_token"]


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