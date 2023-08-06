# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyazo_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<8.0.0', 'pyperclip>=1.7.0,<2.0.0', 'requests>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['pyazo = pyazo_cli.pyazo:upload_image']}

setup_kwargs = {
    'name': 'pyazo-cli',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Jelena Dokic',
    'author_email': 'jrubics@hacke.rs',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
