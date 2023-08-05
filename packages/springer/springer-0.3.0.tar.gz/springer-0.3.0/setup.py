# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['springer']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.45.0,<5.0.0',
 'typer>=0.1.1,<0.2.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['springer = springer.__main__:cli']}

setup_kwargs = {
    'name': 'springer',
    'version': '0.3.0',
    'description': 'Bulk Springer Textbook Downloader',
    'long_description': None,
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
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
