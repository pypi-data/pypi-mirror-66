# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interpolation',
 'interpolation..ipynb_checkpoints',
 'interpolation.multilinear',
 'interpolation.multilinear.tests',
 'interpolation.smolyak',
 'interpolation.smolyak.tests',
 'interpolation.splines',
 'interpolation.splines..ipynb_checkpoints',
 'interpolation.splines.tests',
 'interpolation.tests']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.49.0,<0.50.0', 'numpy>=1.18.3,<2.0.0', 'tempita>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'interpolation',
    'version': '2.1.4',
    'description': 'Interpolation in Python',
    'long_description': None,
    'author': 'Chase Coleman',
    'author_email': 'cc7768@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
