# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proto_square_api']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.11.3,<4.0.0']

setup_kwargs = {
    'name': 'proto-square-api',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jerome Leclanche',
    'author_email': 'jerome@leclan.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
