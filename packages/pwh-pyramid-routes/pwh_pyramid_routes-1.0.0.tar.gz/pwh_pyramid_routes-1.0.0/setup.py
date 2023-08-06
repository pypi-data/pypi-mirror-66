# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pwh_pyramid_routes']

package_data = \
{'': ['*']}

install_requires = \
['decorator>=4.4.2,<5.0.0', 'pyramid_jinja2>=2.8,<3.0']

setup_kwargs = {
    'name': 'pwh-pyramid-routes',
    'version': '1.0.0',
    'description': 'Route helpers for Pyramid',
    'long_description': None,
    'author': 'Mark Hall',
    'author_email': 'mark.hall@work.room3b.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
