# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sp_ask_list_of_concurrent_chats']

package_data = \
{'': ['*']}

install_requires = \
['lh3api>=0.2.0,<0.3.0',
 'numpy>=1.18.2,<2.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'pandas>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'sp-ask-list-of-concurrent-chats',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Guinsly Mondesir',
    'author_email': 'guinslym@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
