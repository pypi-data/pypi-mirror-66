# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kahless']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'gunicorn>=20.0.4,<21.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'parse>=1.15.0,<2.0.0',
 'requests-wsgi-adapter>=0.4.1,<0.5.0',
 'requests>=2.23.0,<3.0.0',
 'webob>=1.8.6,<2.0.0',
 'whitenoise>=5.0.1,<6.0.0']

setup_kwargs = {
    'name': 'kahless',
    'version': '0.1',
    'description': '',
    'long_description': None,
    'author': 'Lech Gudalewicz',
    'author_email': 'lechgu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lechgu/kahless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
