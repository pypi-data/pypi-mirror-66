# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['repamatrix']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.17.4,<2.0.0']

entry_points = \
{'console_scripts': ['repamatrix = repamatrix:main']}

setup_kwargs = {
    'name': 'repamatrix',
    'version': '0.0.1',
    'description': "cmatrix like terminal 'screen saver'",
    'long_description': '# `repamatrix`\n\n`cmatrix` like terminal *screen saver*\n\n## Install\n\n```\n$ pip install repamatrix\n```\n\n## Running\n\n```\n$ repamatrix\n```\n\n',
    'author': 'Gyuri Horak',
    'author_email': 'dyuri@horak.hu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dyuri/repamatrix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
