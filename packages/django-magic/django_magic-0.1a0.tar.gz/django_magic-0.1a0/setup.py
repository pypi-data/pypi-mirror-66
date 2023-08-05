# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_magic']

package_data = \
{'': ['*']}

install_requires = \
['dj_database_url>=0.5.0,<0.6.0', 'django>=3.0.5,<4.0.0']

setup_kwargs = {
    'name': 'django-magic',
    'version': '0.1a0',
    'description': 'A collection of simple helpers and utilities for Django web development',
    'long_description': None,
    'author': 'Jeremy Potter',
    'author_email': 'git@stormdesign.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
