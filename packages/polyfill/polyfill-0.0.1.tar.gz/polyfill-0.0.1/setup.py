# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polyfill']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'polyfill',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jessekrubin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
