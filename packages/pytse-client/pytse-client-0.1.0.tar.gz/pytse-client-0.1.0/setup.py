# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytse_client', 'pytse_client.data', 'pytse_client.examples']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pytse-client',
    'version': '0.1.0',
    'description': 'tehran stock exchange(TSE) client in python',
    'long_description': '',
    'author': 'glyphack',
    'author_email': 'sh.hooshyari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
