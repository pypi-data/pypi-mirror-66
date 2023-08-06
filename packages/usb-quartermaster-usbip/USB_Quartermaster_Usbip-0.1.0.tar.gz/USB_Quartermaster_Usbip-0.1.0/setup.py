# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['USB_Quartermaster_Usbip']

package_data = \
{'': ['*']}

install_requires = \
['USB_Quartermaster_common>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'usb-quartermaster-usbip',
    'version': '0.1.0',
    'description': 'Quartermaster support for managing USBIP devices',
    'long_description': None,
    'author': 'Tim Laurence',
    'author_email': 'timdaman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
