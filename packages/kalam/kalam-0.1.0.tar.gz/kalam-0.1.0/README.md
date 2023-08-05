[![Tests](https://github.com/ankcorp/kalam/workflows/Tests/badge.svg)](https://github.com/ankcorp/kalam/actions?workflow=Tests)
[![codecov](https://codecov.io/gh/AnkCorp/kalam/branch/master/graph/badge.svg)](https://codecov.io/gh/AnkCorp/kalam)
[![PyPI](https://img.shields.io/pypi/v/kalam.svg)](https://pypi.org/project/kalam/)
[![Documentation Status](https://readthedocs.org/projects/kalam-ankcorp/badge/?version=latest)](https://kalam-ankcorp.readthedocs.io/en/latest/?badge=latest)

# Kalam

Superpowers for writing!

## Getting Started


## Developing

### Create a python virtual env

```bash
python -m venv venv     # create python environment
. ./venv/bin/activate    # activate python enviroment
```

### Install poetry

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```
or

```bash
pipx install poetry
```

### Install nox

```bash
pip install nox
```
### Nox

Run tests, lint check, type check, doc tests, coverage
```bash
nox
```
