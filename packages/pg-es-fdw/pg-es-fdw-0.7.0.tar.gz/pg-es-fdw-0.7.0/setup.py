# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pg_es_fdw']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.6.0,<8.0.0']

setup_kwargs = {
    'name': 'pg-es-fdw',
    'version': '0.7.0',
    'description': 'Connect PostgreSQL and Elastic Search with this Foreign Data Wrapper',
    'long_description': None,
    'author': 'Matthew Franglen',
    'author_email': 'matthew@franglen.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
