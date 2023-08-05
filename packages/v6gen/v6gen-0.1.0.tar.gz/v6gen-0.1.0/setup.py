# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['v6gen']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'v6gen',
    'version': '0.1.0',
    'description': 'Simple tool for generating IPv6 addresses randomly or based by the hostname',
    'long_description': None,
    'author': 'Michael Vieira',
    'author_email': 'contact@mvieira.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
