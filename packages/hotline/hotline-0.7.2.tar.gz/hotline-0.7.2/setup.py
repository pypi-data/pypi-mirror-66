# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hotline', 'hotline.contexts', 'hotline.styles', 'hotline.tests']

package_data = \
{'': ['*']}

install_requires = \
['PySide2>=5.14.2,<6.0.0', 'Qt.py>=1.2.5,<2.0.0', 'keyboard>=0.13.5,<0.14.0']

setup_kwargs = {
    'name': 'hotline',
    'version': '0.7.2',
    'description': 'Sublime text like Qt Command Palette',
    'long_description': None,
    'author': 'Dan Bradham',
    'author_email': 'danielbradham@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
