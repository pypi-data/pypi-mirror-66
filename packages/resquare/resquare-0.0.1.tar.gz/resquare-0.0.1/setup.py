# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resquare']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'resquare',
    'version': '0.0.1',
    'description': 'Utility for expanding the frame size of a logo image while preserving the background color of the original image.',
    'long_description': None,
    'author': 'faizanbhat',
    'author_email': 'faizan.bhat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
