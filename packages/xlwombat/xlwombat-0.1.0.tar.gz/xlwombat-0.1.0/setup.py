# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlwombat']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0', 'openpyxl>=3.0.3,<4.0.0']

setup_kwargs = {
    'name': 'xlwombat',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'wiliam chu',
    'author_email': 'chudood@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
