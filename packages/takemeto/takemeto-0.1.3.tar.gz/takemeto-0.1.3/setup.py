# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['takemeto']

package_data = \
{'': ['*']}

install_requires = \
['typer-cli>=0.0.9,<0.0.10', 'typer[all]>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['takemeto = takemeto.main:app']}

setup_kwargs = {
    'name': 'takemeto',
    'version': '0.1.3',
    'description': 'A super tiny package to quickly take you to URL destinations using the command line.',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
