# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['USB_Quartermaster_common']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'usb-quartermaster-common',
    'version': '0.1.0',
    'description': 'Quartermaster library of common code used between client and server',
    'long_description': None,
    'author': 'Tim Laurence',
    'author_email': 'timdaman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
