# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['r2k', 'r2k.cli', 'r2k.cli.config', 'r2k.cli.subscription']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.0,<5.0.0',
 'click>=7.1.1,<8.0.0',
 'feedparser>=5.2.1,<6.0.0',
 'newspaper3k>=0.2.8,<0.3.0',
 'pick>=0.6.7,<0.7.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['r2k = r2k.cli:main']}

setup_kwargs = {
    'name': 'r2k',
    'version': '0.1.0',
    'description': 'A tool that lets you periodically send articles received from an RSS feed to your Kindle',
    'long_description': None,
    'author': 'Pavel Brodsky',
    'author_email': 'mcouthon@gmail.com',
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
