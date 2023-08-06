# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viz', 'vizapi', 'vizbase']

package_data = \
{'': ['*']}

install_requires = \
['funcy>=1.14,<2.0', 'graphenelib>=1.2.0,<2.0.0', 'toolz>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'viz-python-lib',
    'version': '0.1.0',
    'description': 'python library for VIZ blockchain',
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
