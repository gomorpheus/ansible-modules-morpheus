#!/usr/bin/python
import requests
import json
from ansible.module_utils.basic import *
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def main():

    fields = {
        "username": {"default": True, "type": "str"},
        "password": {"default": True, "type": "str"},
        "baseurl": {"default": True, "type": "str"}
    }


    module = AnsibleModule(argument_spec=fields)
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
    module.params.update({"api_token": access_token})

    module.exit_json(changed=False, meta=module.params)




if __name__=="__main__":
    main()
