# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elasticmagic_qf_attrs']

package_data = \
{'': ['*']}

install_requires = \
['elasticmagic>=0.1.0-alpha.12,<0.2.0']

setup_kwargs = {
    'name': 'elasticmagic-qf-attrs',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Alexander Koval',
    'author_email': 'kovalidis@gmail.com',
    'maintainer': 'Alexander Koval',
    'maintainer_email': 'kovalidis@gmail.com',
    'url': 'https://github.com/anti-social/elasticmagic-qf-attrs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
