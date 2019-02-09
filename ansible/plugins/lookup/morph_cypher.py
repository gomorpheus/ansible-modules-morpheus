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


def run(self, terms, variables, **kwargs):
    environments = variables.get('environment', [])


def main(argv=sys.argv[1:]):
    if len(argv) < 1:
        print("Usage: hashivault.py path [key]")
        return -1
    print(LookupModule().run(argv, {})[0])
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
