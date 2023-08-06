# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teamtrain_sdk', 'teamtrain_sdk.trainingpy']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=14.0,<15.0', 'pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['export_all = teamtrain_sdk.teamtrain:main']}

setup_kwargs = {
    'name': 'teamtrain-sdk',
    'version': '0.1.1',
    'description': 'Python tools for interacting with the TeamTrain SDK',
    'long_description': None,
    'author': 'Edd',
    'author_email': 'edward.abrahamsen-mills@safetyculture.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
