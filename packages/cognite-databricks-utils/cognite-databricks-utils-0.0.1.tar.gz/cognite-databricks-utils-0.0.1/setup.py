# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.databricks_utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'databricks-api>=0.4.0,<0.5.0',
 'python-semantic-release>=6.0.1,<7.0.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['db-util = cognite.databricks_utils.cli:run']}

setup_kwargs = {
    'name': 'cognite-databricks-utils',
    'version': '0.0.1',
    'description': 'Utilities for administrating a Databricks shard',
    'long_description': None,
    'author': 'Magnus Moan',
    'author_email': 'magnus.moan@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
