# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['helpers']

package_data = \
{'': ['*']}

modules = \
['netbox_loadtest']
install_requires = \
['openpyxl>=3.0.3,<4.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['netbox-loadtest = netbox_loadtest:start']}

setup_kwargs = {
    'name': 'netbox-loadtest',
    'version': '2.0.1',
    'description': 'A load test script for the netbox IPAM solution.',
    'long_description': None,
    'author': 'Jarrod J Manzer',
    'author_email': 'jjmanzer@godaddy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jjmanzer/netbox-loadtest/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
