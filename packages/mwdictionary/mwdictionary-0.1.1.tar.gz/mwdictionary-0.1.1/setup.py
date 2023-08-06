# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mwdictionary']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'mwdictionary',
    'version': '0.1.1',
    'description': 'API Wrapper for the Merriam-Webster API.',
    'long_description': None,
    'author': 'Peder Hovdan Andresen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
