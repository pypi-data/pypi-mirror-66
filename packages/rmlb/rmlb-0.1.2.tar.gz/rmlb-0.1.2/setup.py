# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rmlb']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rmlb = rmlb:main']}

setup_kwargs = {
    'name': 'rmlb',
    'version': '0.1.2',
    'description': 'Remove a branch that does not exist in remote.',
    'long_description': "# rmlb\n\nRemove a branch that does not exist in remote.\n\n## Install\n\n```shell\n$ pip install rmlb\n```\n\n## Usage\n\n```no\nusage: rmlb.py [-h] [-ro {-d,-D}] [-q]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -ro {-d,-D}, --remove-option {-d,-D}\n                        Options for removing a branch. The default is '-d'.\n  -q, --quiet           No output.\n```\n\n## Author\nucpr\n\n## License\nMIT\n",
    'author': 'ucpr',
    'author_email': 'hoge.uchihara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ucpr/rmlb',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
