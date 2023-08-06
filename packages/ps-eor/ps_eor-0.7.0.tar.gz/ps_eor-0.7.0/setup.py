# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ps_eor', 'ps_eor.tests', 'ps_eor.tools']

package_data = \
{'': ['*']}

install_requires = \
['GPy>=1.9,<2.0',
 'backports-functools_lru_cache>=1.5,<2.0',
 'click>=7.1.1,<8.0.0',
 'configparser>=4.0,<5.0',
 'healpy>=1.12,<2.0',
 'pyfftw>=0.12,<0.13',
 'scikit-learn>=0.20,<0.21',
 'tables>=3.2,<4.0']

extras_require = \
{':python_version >= "2.7" and python_version < "3.0"': ['astropy>=2,<3',
                                                         'numpy>=1.16,<2.0',
                                                         'scipy>=1.2,<2.0',
                                                         'matplotlib>=2,<3',
                                                         'reproject>=0.5,<0.6'],
 ':python_version >= "3.6" and python_version < "4.0"': ['astropy>=4,<5',
                                                         'numpy>=1.18,<2.0',
                                                         'scipy>=1.4,<2.0',
                                                         'matplotlib>=3,<4',
                                                         'reproject>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['pstool = ps_eor.tools.pstool:main']}

setup_kwargs = {
    'name': 'ps-eor',
    'version': '0.7.0',
    'description': 'Foreground modeling/removal and Power Spectra generation',
    'long_description': None,
    'author': 'Florent Mertens',
    'author_email': 'flomertens@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
