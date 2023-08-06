# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unionfind']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unionfind',
    'version': '0.0.11',
    'description': '`unionfind` is a package for unionfind.',
    'long_description': '`unionfind` is a package for unionfind.\n\n::\n\n   from unionfind import unionfind\n   u = unionfind(3) # There are 3 items.\n   u.unite(0, 2) # Set 0 and 2 to same group.\n   u.issame(1, 2) # Ask "Are 1 and 2 same?"\n   u.groups() # Return groups.\n\nSee also https://pypi.org/project/ortoolpy/\n\nRequirements\n------------\n* Python 3\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install unionfind\n\nHistory\n-------\n0.0.1 (2015-4-3)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/unionfind',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
