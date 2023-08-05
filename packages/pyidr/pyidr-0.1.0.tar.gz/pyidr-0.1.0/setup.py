# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyidr']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.1,<2.0.0',
 'scipy>=1.4.1,<2.0.0',
 'statsmodels>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'pyidr',
    'version': '0.1.0',
    'description': 'Python implementation of the irreproducible discovery rate',
    'long_description': None,
    'author': 'Fabian Hausmann',
    'author_email': 'fabian.hausmann@zmnh.uni-hamburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
