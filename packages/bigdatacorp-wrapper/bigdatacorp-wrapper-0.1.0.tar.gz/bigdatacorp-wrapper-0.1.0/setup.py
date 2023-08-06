# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigdatacorp_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['python-decouple>=3.3,<4.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'bigdatacorp-wrapper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ricardo Gaya',
    'author_email': 'rrgaya@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
