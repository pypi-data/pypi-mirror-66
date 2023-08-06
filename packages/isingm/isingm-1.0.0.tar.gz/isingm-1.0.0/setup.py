# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isingm']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'numpy>=1.18.2,<2.0.0']

setup_kwargs = {
    'name': 'isingm',
    'version': '1.0.0',
    'description': 'A pythonic Ising model simulation',
    'long_description': None,
    'author': 'Pacidus',
    'author_email': 'pacidus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
