# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scproxymesh']

package_data = \
{'': ['*']}

install_requires = \
['scrapy>=1.6', 'six>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'scrapy-proxymesh-py3',
    'version': '0.0.5',
    'description': 'Proxymesh downloader middleware for Scrapy',
    'long_description': None,
    'author': 'mizhgun',
    'author_email': 'mizhgun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
