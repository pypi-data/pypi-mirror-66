# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brewblox_dev']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'python-dotenv>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'brewblox-dev',
    'version': '1.6.0',
    'description': 'Brewblox development tools',
    'long_description': None,
    'author': 'BrewPi',
    'author_email': 'development@brewpi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
