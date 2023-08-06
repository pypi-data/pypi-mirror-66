# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_slack', 'async_slack.orger']

package_data = \
{'': ['*']}

install_requires = \
['bonobo>=0.6.4,<0.7.0',
 'dpath>=2.0.1,<3.0.0',
 'emoji>=0.5.4,<0.6.0',
 'slacker>=0.14.0,<0.15.0',
 'tenacity>=6.1.0,<7.0.0',
 'toml>=0.10.0,<0.11.0',
 'workalendar>=8.4.0,<9.0.0']

entry_points = \
{'console_scripts': ['async-update-slack = async_slack.update_database:main']}

setup_kwargs = {
    'name': 'async-slack',
    'version': '0.1.0rc1',
    'description': '',
    'long_description': None,
    'author': 'Pascal Bugnion',
    'author_email': 'pascal@bugnion.org',
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
