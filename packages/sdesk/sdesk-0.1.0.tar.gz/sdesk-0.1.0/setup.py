# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdesk', 'sdesk.proc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sdesk',
    'version': '0.1.0',
    'description': 'ScienceDesk helper library',
    'long_description': None,
    'author': 'ScienceDesk GmbH',
    'author_email': 'github@sciencedesk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
