# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gofuncyourself']
setup_kwargs = {
    'name': 'gofuncyourself',
    'version': '0.1.0',
    'description': 'Go-like error handling, but with a twist',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
