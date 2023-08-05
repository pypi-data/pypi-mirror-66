# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytchout', 'pytchout.analysis', 'pytchout.tools']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.2,<2.0.0', 'pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pytchout',
    'version': '0.1.0',
    'description': 'A package for downloading baseball data and performing baseball data analytics in Python.',
    'long_description': None,
    'author': 'Josh Hejka',
    'author_email': 'josh@joshhejka.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
