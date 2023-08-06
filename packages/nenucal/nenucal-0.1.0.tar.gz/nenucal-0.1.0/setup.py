# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nenucal', 'nenucal.tests', 'nenucal.tools']

package_data = \
{'': ['*'], 'nenucal': ['cal_config/*', 'templates/*']}

install_requires = \
['astropy>=4.0,<5.0',
 'asyncssh>=2.1,<3.0',
 'click>=7.0,<8.0',
 'matplotlib>=3.0,<4.0',
 'progressbar2>=3.0,<4.0',
 'python-casacore>=3.2.0,<4.0.0',
 'scipy>=1.4,<2.0',
 'tables>=3.2,<4.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['calpipe = nenucal.tools.calpipe:main',
                     'flagtool = nenucal.tools.flagtool:main',
                     'soltool = nenucal.tools.soltool:main']}

setup_kwargs = {
    'name': 'nenucal',
    'version': '0.1.0',
    'description': 'Calibration pipeline for the NenuFAR Cosmic Dawn project',
    'long_description': None,
    'author': '"Florent Mertens"',
    'author_email': '"florent.mertens@gmail.com"',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
