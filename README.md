# Ansible Modules Morpheus
[![PyPi](https://img.shields.io/pypi/v/ansible-modules-morpheus.svg)](https://pypi.python.org/pypi/ansible-modules-morpheus/) [![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
If you choose to use env vars the following variables can be exported to the environment where you run ansible in order to authenticate to your Morpheus Appliance:
* MORPH_ADDR : url for Morpheus Appliance
* MORPH_AUTHTYPE: authorization type for Morpheus (token or userpass)
* MORPH_USER: Morpheus appliance username for userpass authtype
* MORPH_PASSWORD: Morpheus appliance user password for userpass authtype
* MORPH_TOKEN: Morpheus api token for token authtype

Addition variables for specific modules:
* MORPH_SECRET: Morpheus secret key for Cypher value reads in morph_cypher module

## Arguments
Alternatively you can pass arguments to the module by using discrete variables in your task module.  Args that are supported are:
* baseurl: url for Morpheus Appliance
* authtype: authorization type for Morpheus (token or userpass)
* api_token: Morpheus api token for token authtype
* username: Morpheus appliance username for userpass authtype
* password: Morpheus appliance user password for userpass authtype

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

## License
[MIT](https://github.com/gomorpheus/ansible-modules-morpheus/blob/master/LICENSE)