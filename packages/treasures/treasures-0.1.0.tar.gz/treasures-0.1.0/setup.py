# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treasures']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'treasures',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'SimpleBet',
    'author_email': 'team@simplebet.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
