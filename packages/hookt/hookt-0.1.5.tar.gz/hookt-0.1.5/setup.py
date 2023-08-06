# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['hookt']
install_requires = \
['anyio>=1.2.3,<2.0.0', 'wrapt>=1.11.2,<2.0.0']

setup_kwargs = {
    'name': 'hookt',
    'version': '0.1.5',
    'description': 'Asynchronous function hooks using decorators.',
    'long_description': '<p align="center">\n  <a href="https://pypi.org/project/hookt" alt="PyPI">\n    <img src="https://img.shields.io/pypi/v/hookt"/></a>\n  <a alt="Dependencies">\n    <img alt="Libraries.io dependency status for latest release" src="https://img.shields.io/librariesio/release/pypi/hookt"></a>\n  <a href="https://travis-ci.com/nanananisore/hookt" alt="Build Status">\n    <img src="https://travis-ci.com/nanananisore/hookt.svg?branch=master"/></a>\n  <a alt="License">\n    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/hookt"></a>\n</p>\n\n`hookt` is an asynchronous event framework utilizing decorators.\nIt uses `anyio`, so it is compatible with `asyncio`, `curio` and `trio`.\nFor an up-to-date list of compatible backends,\nsee [`anyio`](https://github.com/agronholm/anyio)\n\n## installation\n`pip install hookt`\n',
    'author': 'nanananisore',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nanananisore/hookt',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
