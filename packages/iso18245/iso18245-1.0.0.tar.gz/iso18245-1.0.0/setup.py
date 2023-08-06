# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iso18245']

package_data = \
{'': ['*'], 'iso18245': ['data/*']}

setup_kwargs = {
    'name': 'iso18245',
    'version': '1.0.0',
    'description': 'ISO 18245 Merchant Category Codes database',
    'long_description': None,
    'author': 'Jerome Leclanche',
    'author_email': 'jerome@leclan.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
