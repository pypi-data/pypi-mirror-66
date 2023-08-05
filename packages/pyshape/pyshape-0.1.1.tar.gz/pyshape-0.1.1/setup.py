# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyshape']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyshape',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'yafeunteun',
    'author_email': 'yfe.github@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
