# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'icon',
    'version': '0.0.4',
    'description': 'Random choice from Google Material Icons in Jupyter notebook',
    'long_description': 'Random choice from Google Material Icons in Jupyter notebook\n\n* import icon\n\n* %icon\n\nSee: https://github.com/google/material-design-icons',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/icon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
