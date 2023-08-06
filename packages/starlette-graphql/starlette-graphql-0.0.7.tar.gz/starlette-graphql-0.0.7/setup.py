# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stargql']

package_data = \
{'': ['*']}

install_requires = \
['python-gql<0.1', 'starlette>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'starlette-graphql',
    'version': '0.0.7',
    'description': 'The starlette GraphQL implement, which  support query, mutate and subscription.',
    'long_description': None,
    'author': 'syfun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/syfun/starlette-graphql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
