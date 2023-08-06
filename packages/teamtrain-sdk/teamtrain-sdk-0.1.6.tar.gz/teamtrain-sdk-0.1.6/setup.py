# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teamtrain_sdk',
 'teamtrain_sdk.lib.python3.7.site-packages',
 'teamtrain_sdk.lib.python3.7.site-packages.pip',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal.cli',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal.commands',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal.distributions',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal.models',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal.operations',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal.req',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal.utils',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._internal.vcs',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.cachecontrol',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.cachecontrol.caches',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.certifi',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.chardet',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.chardet.cli',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.colorama',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.distlib',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.distlib._backport',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.html5lib',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.html5lib._trie',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.html5lib.filters',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.html5lib.treeadapters',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.html5lib.treebuilders',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.html5lib.treewalkers',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.idna',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.lockfile',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.msgpack',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.packaging',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.pep517',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.pkg_resources',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.progress',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.pytoml',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.requests',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.urllib3',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.urllib3.contrib',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.urllib3.contrib._securetransport',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.urllib3.packages',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.urllib3.packages.backports',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.urllib3.packages.rfc3986',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.urllib3.packages.ssl_match_hostname',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.urllib3.util',
 'teamtrain_sdk.lib.python3.7.site-packages.pip._vendor.webencodings',
 'teamtrain_sdk.lib.python3.7.site-packages.pkg_resources',
 'teamtrain_sdk.lib.python3.7.site-packages.pkg_resources._vendor',
 'teamtrain_sdk.lib.python3.7.site-packages.pkg_resources._vendor.packaging',
 'teamtrain_sdk.lib.python3.7.site-packages.pkg_resources.extern',
 'teamtrain_sdk.lib.python3.7.site-packages.setuptools',
 'teamtrain_sdk.lib.python3.7.site-packages.setuptools._vendor',
 'teamtrain_sdk.lib.python3.7.site-packages.setuptools._vendor.packaging',
 'teamtrain_sdk.lib.python3.7.site-packages.setuptools.command',
 'teamtrain_sdk.lib.python3.7.site-packages.setuptools.extern',
 'teamtrain_sdk.trainingpy']

package_data = \
{'': ['*'],
 'teamtrain_sdk': ['bin/*'],
 'teamtrain_sdk.lib.python3.7.site-packages': ['pip-19.2.3.dist-info/*',
                                               'setuptools-41.2.0.dist-info/*']}

install_requires = \
['coloredlogs>=14.0,<15.0', 'pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['export_all = teamtrain_sdk.teamtrain:main']}

setup_kwargs = {
    'name': 'teamtrain-sdk',
    'version': '0.1.6',
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
