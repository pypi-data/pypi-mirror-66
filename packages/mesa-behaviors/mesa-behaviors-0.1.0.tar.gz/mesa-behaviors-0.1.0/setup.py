# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mesa_behaviors',
 'mesa_behaviors.agents',
 'mesa_behaviors.history',
 'mesa_behaviors.models',
 'mesa_behaviors.strategies',
 'mesa_behaviors.utility']

package_data = \
{'': ['*']}

install_requires = \
['bitarray>=1.2.1,<2.0.0',
 'codecov>=2.0.22,<3.0.0',
 'mesa>=0.8.6,<0.9.0',
 'python-semantic-release>=5.2.0,<6.0.0',
 'tox>=3.14.6,<4.0.0']

setup_kwargs = {
    'name': 'mesa-behaviors',
    'version': '0.1.0',
    'description': 'A framework for developing shareable Mesa Agents, Models and creating extensible Utility functions',
    'long_description': '![CI](https://github.com/tokesim/mesa_behaviors/workflows/CI/badge.svg)',
    'author': 'Zane Starr',
    'author_email': 'zcstarr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tokesim/mesa_behaviors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
