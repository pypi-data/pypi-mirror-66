# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitslice']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bitslice',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'zegervdv',
    'author_email': 'zegervdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
