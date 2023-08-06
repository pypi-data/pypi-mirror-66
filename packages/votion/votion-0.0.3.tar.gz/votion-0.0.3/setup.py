# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['votion', 'votion.tests']

package_data = \
{'': ['*']}

install_requires = \
['docker>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['votion = votion.main:main']}

setup_kwargs = {
    'name': 'votion',
    'version': '0.0.3',
    'description': 'Docker image build tool',
    'long_description': '# votion\n\n[![Build Status](https://travis-ci.org/weastur/votion.svg?branch=master)](https://travis-ci.org/weastur/votion)\n[![codecov](https://codecov.io/gh/weastur/votion/branch/master/graph/badge.svg)](https://codecov.io/gh/weastur/votion)\n[![PyPi version](https://img.shields.io/pypi/v/votion.svg)](https://pypi.org/project/votion/)\n[![Python versions](https://img.shields.io/pypi/pyversions/votion)](https://pypi.org/project/votion/)\n[![MIT License](https://img.shields.io/github/license/weastur/votion)](https://github.com/weastur/votion/blob/master/LICENSE)\n[![Open PR](https://img.shields.io/github/issues-pr-raw/weastur/votion)](https://github.com/weastur/votion/pulls)\n[![Open Issues](https://img.shields.io/github/issues-raw/weastur/votion)](https://github.com/weastur/votion/issues)\n[![black-formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/) [![Join the chat at https://gitter.im/votion-build-tool/community](https://badges.gitter.im/votion-build-tool/community.svg)](https://gitter.im/votion-build-tool/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\n---\n\nDocker image build tool\n',
    'author': 'Pavel Sapezhko',
    'author_email': 'me@weastur.com',
    'maintainer': 'Pavel Sapezhko',
    'maintainer_email': 'me@weastur.com',
    'url': 'https://github.com/weastur/votion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
