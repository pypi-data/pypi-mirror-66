# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yinasrun']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['yin = helloworld:run']}

setup_kwargs = {
    'name': 'yinasrun',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'italian roast',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
