# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ariadne_extended',
 'ariadne_extended.cursor_pagination',
 'ariadne_extended.filters',
 'ariadne_extended.graph_loader',
 'ariadne_extended.payload',
 'ariadne_extended.resolvers',
 'ariadne_extended.uuid']

package_data = \
{'': ['*']}

install_requires = \
['ariadne>=0.11.0,<0.12.0', 'pyhumps>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'ariadne-extended',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Patrick Forringer',
    'author_email': 'pforringer@patriotrc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
