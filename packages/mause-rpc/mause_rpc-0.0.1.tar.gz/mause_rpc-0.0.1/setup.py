# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mause_rpc']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.1,<0.4.0', 'pika>=1.1.0,<2.0.0', 'retry>=0.9.2,<0.10.0']

entry_points = \
{'console_scripts': ['publish = mause_rpc:publish']}

setup_kwargs = {
    'name': 'mause-rpc',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Elliana May',
    'author_email': 'me@mause.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
