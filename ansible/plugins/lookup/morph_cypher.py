#!/usr/bin/env python
#
# Vault Lookup Plugin
#
# A simple example of using the vault plugin in a role:
#    ---
#    - debug: msg="{{lookup('vault', 'ldapadmin', 'password')}}"
#
# The plugin must be run with VAULT_ADDR and VAULT_TOKEN set and
# exported.
#
# The plugin can be run manually for testing:
#     python ansible/plugins/lookup/hashivault.py ldapadmin password
#

import json
import os
import requests
import sys
import warnings

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.morpheus import (
    morphtoken,
    morph_get_client,
)


class LookupModule(LookupBase):
    
    def _get_environment(self, environments, name, default_value=None):
        for env in environments:
            if name in env:
                return env.get(name)
        return os.getenv(name, default_value)