# Ansible Modules Morpheus
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
The following variables need to be exported to the environment where you run ansible in order to authenticate to your Morpheus Appliance:
>*MORPH_ADDR : url for Morpheus Appliance
>*MORPH_AUTHTYPE: authorization type for Morpheus (token or userpass)