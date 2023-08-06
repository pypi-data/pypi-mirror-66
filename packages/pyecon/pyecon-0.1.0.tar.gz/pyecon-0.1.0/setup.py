# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyecon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyecon',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Fan Wang',
    'author_email': 'wangfanbsg75@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
