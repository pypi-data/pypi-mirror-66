# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kalam']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.3.0,<4.0.0',
 'requests>=2.22.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0']}

entry_points = \
{'console_scripts': ['kalam = kalam.console:main']}

setup_kwargs = {
    'name': 'kalam',
    'version': '0.1.0',
    'description': 'Superpowers for writing!',
    'long_description': '[![Tests](https://github.com/ankcorp/kalam/workflows/Tests/badge.svg)](https://github.com/ankcorp/kalam/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/AnkCorp/kalam/branch/master/graph/badge.svg)](https://codecov.io/gh/AnkCorp/kalam)\n[![PyPI](https://img.shields.io/pypi/v/kalam.svg)](https://pypi.org/project/kalam/)\n[![Documentation Status](https://readthedocs.org/projects/kalam-ankcorp/badge/?version=latest)](https://kalam-ankcorp.readthedocs.io/en/latest/?badge=latest)\n\n# Kalam\n\nSuperpowers for writing!\n\n## Getting Started\n\n\n## Developing\n\n### Create a python virtual env\n\n```bash\npython -m venv venv     # create python environment\n. ./venv/bin/activate    # activate python enviroment\n```\n\n### Install poetry\n\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n```\nor\n\n```bash\npipx install poetry\n```\n\n### Install nox\n\n```bash\npip install nox\n```\n### Nox\n\nRun tests, lint check, type check, doc tests, coverage\n```bash\nnox\n```\n',
    'author': 'Ank',
    'author_email': 'ank@ankcorp.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ankcorp/kalam',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
