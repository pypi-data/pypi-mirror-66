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
    'version': '0.1.2',
    'description': '',
    'long_description': "# Take Snapshot of WebPage\n\n```bash\n# install\n$ pip install websnapshot\n\n# better install\n$ pipx install websnapshot\n\n# from stdout\n$ echo 'https://stackoverflow.com/' | websnapshot\n\n# text file with urls\n$ websnapshot -i urls.txt\n\n# usage\n$ websnapshot --help\n```\n",
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
