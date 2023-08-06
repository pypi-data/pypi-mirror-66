# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyazo_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'pyperclip>=1.8.0,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['pyazo = pyazo_cli.pyazo:upload_image']}

setup_kwargs = {
    'name': 'pyazo-cli',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jelena Dokic',
    'author_email': 'jelena.dpk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
