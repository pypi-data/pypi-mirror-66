# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_openapi_ng']

package_data = \
{'': ['*']}

install_requires = \
['inflection', 'pydantic']

entry_points = \
{'console_scripts': ['openapigen = pydantic_openapi_ng.command_line:main']}

setup_kwargs = {
    'name': 'pydantic-openapi-ng',
    'version': '0.2.1',
    'description': 'Generate OpenAPI schema from pydantic models',
    'long_description': None,
    'author': 'Yury Blagoveshchenskiy',
    'author_email': 'yurathestorm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
