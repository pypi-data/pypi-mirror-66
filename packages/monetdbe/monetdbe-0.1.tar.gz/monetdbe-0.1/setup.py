# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monetdbe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'monetdbe',
    'version': '0.1',
    'description': 'MonetDBe - the Python embedded MonetDB',
    'long_description': '# monetdbe\nMonetDBe - the Python embedded MonetDB\n',
    'author': 'Gijs Molenaar',
    'author_email': 'gijs@pythonic.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gijzelaerr/monetdbe',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
