# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['websnapshot']

package_data = \
{'': ['*'], 'websnapshot': ['websnapshots/*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'pyppeteer>=0.0.25,<0.0.26']

entry_points = \
{'console_scripts': ['websnapshot = websnapshot:websnapshot']}

setup_kwargs = {
    'name': 'websnapshot',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
