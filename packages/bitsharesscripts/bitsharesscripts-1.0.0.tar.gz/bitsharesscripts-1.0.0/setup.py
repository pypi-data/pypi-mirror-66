# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitsharesscripts']

package_data = \
{'': ['*']}

install_requires = \
['bitshares>=0.4.0,<0.5.0', 'click>=7.1.1,<8.0.0', 'uptick>=0.2.4,<0.3.0']

setup_kwargs = {
    'name': 'bitsharesscripts',
    'version': '1.0.0',
    'description': 'A set of scripts for BitShares',
    'long_description': None,
    'author': 'Vladimir Kamarzin',
    'author_email': 'vvk@vvk.pp.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
