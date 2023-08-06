# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['knapsack']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'knapsack',
    'version': '0.0.6',
    'description': '`knapsack` is a package for for solving knapsack problem.',
    'long_description': '`knapsack` is a package for solving knapsack problem.\nMaximize sum of selected weight.\nSum of selected size is les than capacity.\nAlgorithm: Dynamic Optimization\n::\n\n   import knapsack\n   size = [21, 11, 15, 9, 34, 25, 41, 52]\n   weight = [22, 12, 16, 10, 35, 26, 42, 53]\n   capacity = 100\n   knapsack.knapsack(size, weight).solve(capacity)\n\nSee also https://pypi.org/project/ortoolpy/\n\nRequirements\n------------\n* Python 3\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install knapsack\n\nHistory\n-------\n0.0.1 (2015-6-26)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/knapsack',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
