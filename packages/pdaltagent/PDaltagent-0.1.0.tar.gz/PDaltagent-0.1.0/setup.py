# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdaltagent']

package_data = \
{'': ['*'], 'pdaltagent': ['scripts/*']}

install_requires = \
['celery[redis]>=4.4.2,<5.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['pd-send = pdaltagent.pdsend:main',
                     'pdagentd = pdaltagent.tasks:consume']}

setup_kwargs = {
    'name': 'pdaltagent',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Martin Stone',
    'author_email': 'martindstone@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
