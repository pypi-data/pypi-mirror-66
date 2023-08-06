# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coronatank']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=1.9.6,<2.0.0']

setup_kwargs = {
    'name': 'coronatank',
    'version': '0.1.0',
    'description': 'A small tank game based on pygame.',
    'long_description': None,
    'author': 'Sylvain Roy',
    'author_email': 'sylvain.roy@m4x.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.7,<4.0.0',
}


setup(**setup_kwargs)
