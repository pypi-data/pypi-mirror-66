# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sedge']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sedge',
    'version': '2.1.0',
    'description': 'Template and share OpenSSH ssh_config files.',
    'long_description': None,
    'author': 'Grahame Bowland',
    'author_email': 'grahame@oreamnos.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
