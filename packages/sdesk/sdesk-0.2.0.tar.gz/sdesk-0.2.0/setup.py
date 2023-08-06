# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sdesk', 'sdesk.api', 'sdesk.proc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'sdesk',
    'version': '0.2.0',
    'description': 'ScienceDesk helper library',
    'long_description': '# ScienceDesk Python helpers\n\nThis module provides Python code to help you interact with and extend the\nScienceDesk platform.\n\n## Modules\n\n- api: helpers to interact with the ScienceDesk API\n- proc: helpers to write ScienceDesk algorithms\n',
    'author': 'ScienceDesk GmbH',
    'author_email': 'github@sciencedesk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sciencedesk.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
