# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algovis']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'algovis',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'hotshot07',
    'author_email': 'aroram@tcd.ie',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
