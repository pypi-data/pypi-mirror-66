# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_pro']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'deepl-pro',
    'version': '0.1.4',
    'description': 'A wrapper for the DeepL Pro API.',
    'long_description': None,
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
