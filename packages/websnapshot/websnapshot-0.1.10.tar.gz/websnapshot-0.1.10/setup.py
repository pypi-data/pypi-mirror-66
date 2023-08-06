# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['websnapshot']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'pyppeteer>=0.0.25,<0.0.26']

entry_points = \
{'console_scripts': ['websnapshot = websnapshot:websnapshot']}

setup_kwargs = {
    'name': 'websnapshot',
    'version': '0.1.10',
    'description': 'Python command-line tool for capture snapshots of web pages using Headless Chromium.',
    'long_description': '# WebSnapshot\n\n🐍 Python command-line tool for capture 📷 snapshots of web pages using Headless Chromium.\n\nFeatures:\n\n- Change viewport size;\n- Full page snaphots;\n- Custom headers and other (see `--help`).\n\n```bash\n# install\n$ pip install websnapshot\n\n# install in isolated environment using pipx\n$ pipx install websnapshot\n\n# full page snapshot\n$ echo "https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8" | websnapshot --full_page\n\n# file with urls, each on a new line\n$ websnapshot -i urls.txt\n\n# help\n$ websnapshot --help\n```\n',
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tz4678/websnapshot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
