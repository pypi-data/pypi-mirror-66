# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quartermaster_client',
 'quartermaster_client.client',
 'quartermaster_client.client.integration']

package_data = \
{'': ['*']}

install_requires = \
['usb-quartermaster-common>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['quartermaster_client = '
                     'quartermaster_client.__main__:run']}

setup_kwargs = {
    'name': 'usb-quartermaster-client',
    'version': '0.1.1',
    'description': 'Client to connect USB devices managed by Quartermaster Server',
    'long_description': None,
    'author': 'Tim Laurence',
    'author_email': 'timdaman@gmail.com',
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
