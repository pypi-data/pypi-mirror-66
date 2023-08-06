# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dual']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dual = dual:main']}

setup_kwargs = {
    'name': 'dual',
    'version': '0.0.9',
    'description': '`dual` is a package for dual problem.',
    'long_description': '`dual` is a package for dual problem.\n::\n\n   from dual import dual\n   print(dual("min c^T x\\nA x >= b\\nx >= 0"))\n\nRequirements\n------------\n* Python 3\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install dual\n\nHistory\n-------\n0.0.1 (2016-3-27)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/dual',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
