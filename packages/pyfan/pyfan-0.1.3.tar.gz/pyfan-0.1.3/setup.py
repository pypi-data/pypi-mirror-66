# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfan', 'pyfan.util', 'pyfan.util.rmd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfan',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Fan Wang',
    'author_email': 'wangfanbsg75@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
