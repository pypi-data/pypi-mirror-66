# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dyndb']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.26,<2.0.0', 'click>=7.1.1,<8.0.0']

entry_points = \
{'console_scripts': ['dyndb = dyndb.cli:main']}

setup_kwargs = {
    'name': 'dyndb',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pascal Prins',
    'author_email': 'pascal.prins@foobar-it.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
