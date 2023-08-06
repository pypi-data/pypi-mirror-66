# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['loopr']
setup_kwargs = {
    'name': 'loopr',
    'version': '0.1',
    'description': 'Loopr python client',
    'long_description': None,
    'author': 'Subhankar',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
