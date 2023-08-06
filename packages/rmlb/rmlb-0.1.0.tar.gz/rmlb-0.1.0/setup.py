# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rmlb']
entry_points = \
{'console_scripts': ['rmlb = rmlb:main']}

setup_kwargs = {
    'name': 'rmlb',
    'version': '0.1.0',
    'description': 'Remove a branch that does not exist in remote.',
    'long_description': None,
    'author': 'ucpr',
    'author_email': 'hoge.uchihara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
