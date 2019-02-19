# Ansible Modules Morpheus
[![Latest Version](https://img.shields.io/pypi/v/ansible-modules-morpheus.svg)](https://pypi.python.org/pypi/ansible-modules-morpheus/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Install this module:
* via `pip`
```python
pip install ansible-modules-morpheus
```
* via `ansible-galaxy`
```python
ansible-galaxy install 'git+https://github.com/gomorpheus/ansible-modules-morpheus.git'
```
## Environment Variables
If you choose to use env vars the following variables can be exported to the environment you are controlling with ansible in order to authenticate to your Morpheus Appliance:
* MORPH_ADDR : url for Morpheus Appliance
* MORPH_AUTHTYPE: authorization type for Morpheus (token or userpass)
* MORPH_USER: Morpheus appliance username for userpass authtype
* MORPH_PASSWORD: Morpheus appliance user password for userpass authtype
* MORPH_TOKEN: Morpheus api token for token authtype
* MORPH_SSL_VERIFY: Boolean for verifying ssl

Addition variables for specific modules:
* MORPH_SECRET: Morpheus secret key for Cypher value reads in morph_cypher module

## Arguments
Alternatively you can pass arguments to the module by using discrete variables in your task module.  Args that are supported are:
* baseurl: url for Morpheus Appliance
* authtype: authorization type for Morpheus (token or userpass)
* api_token: Morpheus api token for token authtype
* username: Morpheus appliance username for userpass authtype
* password: Morpheus appliance user password for userpass authtype
* ssl_verify: Boolean for verifying SSL

For specific modules
* secret_key: Morpheus secret key for Cypher value reads in morph_cypher module

## Module Examples
### morph_cypher
```python
- hosts: foo
  tasks:
    - name: gettoken
      morph_cypher:
        baseurl: "https://sandbox.morpheusdata.com"
        secret_key: "password/spark"
        authtype: token
        ssl_verify: False
      register: results
    - debug: var=results.secret
```
or explicitly passing the api_token as a var:
```python
- hosts: foo
  tasks:
    - name: gettoken
      morph_cypher:
        baseurl: "https://sandbox.morpheusdata.com"
        secret_key: "secret/nooneknows"
        authtype: token
        api_token: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      register: results
```

## Lookup Plugin Examples
### morph_cypher
```python
- debug:
    msg: "{{ lookup('morph_cypher', 'baseurl=https://sandbox.morpheusdata.com authtype=token api_token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx secret_key=password/spark')}}"

- debug:
    msg: "{{ lookup('morph_cypher', 'baseurl=https://sandbox.morpheusdata.com authtype=userpass username=slim_shady password=password secret_key=secret/hello') }}"

- debug:
    msg: "{{ lookup('morph_cypher', 'baseurl=https://sandbox.morpheusdata.com authtype=token api_token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx ssl_verify=False secret_key=key/256/myKey') }}"
```

## License
[MIT](https://github.com/gomorpheus/ansible-modules-morpheus/blob/master/LICENSE)