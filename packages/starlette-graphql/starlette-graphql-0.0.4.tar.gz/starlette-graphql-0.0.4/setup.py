# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stargql']

package_data = \
{'': ['*']}

install_requires = \
['python-gql>=0.0.8,<0.0.9', 'starlette>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'starlette-graphql',
    'version': '0.0.4',
    'description': 'Starlette graphql extension.',
    'long_description': None,
    'author': 'syfun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
