# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tgtg']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.23.0']

setup_kwargs = {
    'name': 'tgtg',
    'version': '0.1.0',
    'description': 'Unoffical python client for TooGoodToGo API',
    'long_description': None,
    'author': 'Anthony Hivert',
    'author_email': 'anthony.hivert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
