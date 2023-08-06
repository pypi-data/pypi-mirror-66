# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiogram-cli',
    'version': '0.0.1a0',
    'description': '',
    'long_description': None,
    'author': 'Alex Root Junior',
    'author_email': 'jroot.junior@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
