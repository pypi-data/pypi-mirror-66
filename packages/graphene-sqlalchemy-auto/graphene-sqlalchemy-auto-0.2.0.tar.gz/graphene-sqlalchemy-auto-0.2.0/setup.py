# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_sqlalchemy_auto']

package_data = \
{'': ['*']}

install_requires = \
['graphene-sqlalchemy>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'graphene-sqlalchemy-auto',
    'version': '0.2.0',
    'description': 'graphene-sqlalchemy-auto',
    'long_description': None,
    'author': 'golden',
    'author_email': 'goodking_bq@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
