# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stoltzmaniac',
 'stoltzmaniac.data_handler',
 'stoltzmaniac.models',
 'stoltzmaniac.models.supervised',
 'stoltzmaniac.models.unsupervised',
 'stoltzmaniac.utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'stoltzmaniac',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Scott Stoltzman',
    'author_email': 'info@stoltzmanconsulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
