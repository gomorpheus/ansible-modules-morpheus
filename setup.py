#!/usr/bin/env python
from setuptools import setup

py_files = [
    "ansible/module_utils/morpheus",
    "ansible/plugins/lookup/morph_cypher"
]
files = [
    "ansible/modules/morpheus",
]

long_description=open('README.md', 'r').read()

setup(
    name='ansible-modules-morpheus',
    version='0.2.0',
    description='Ansible Modules for Morpheus Data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Adam Hicks',
    author_email='ahicks@morpheusdata.com',
    url='https://github.com/gomorpheus/ansible-modules-morpheus',
    py_modules=py_files,
    packages=files,
    install_requires = [
        'ansible>=2.0.0',
        'requests>=2.21.0'
    ],
)
