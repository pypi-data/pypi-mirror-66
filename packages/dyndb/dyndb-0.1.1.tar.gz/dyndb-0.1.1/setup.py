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
    'version': '0.1.1',
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
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
