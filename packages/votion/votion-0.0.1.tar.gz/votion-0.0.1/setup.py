# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['votion', 'votion.tests']

package_data = \
{'': ['*']}

install_requires = \
['docker>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'votion',
    'version': '0.0.1',
    'description': 'Docker image build tool',
    'long_description': None,
    'author': 'Pavel Sapezhko',
    'author_email': 'me@weastur.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
