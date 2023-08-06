# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['call_graph']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['call-graph = call_graph:main']}

setup_kwargs = {
    'name': 'call-graph',
    'version': '0.0.1',
    'description': '`call-graph` is a package for viewing call graph.',
    'long_description': '`call-graph` is a package for viewing call graph.\n::\n\n   $ call-graph\n   usage: call-graph module func\n   \n   $ call-graph call_graph main\n   main\n   ├ get_call_graph\n   │└ getclosurevars\n   │\u3000├ ismethod\n   │\u3000├ isfunction\n   │\u3000└ ismodule\n   └ call_graph_view\n   \u3000└ pairwise\n\n* "no_target" is used for ignoring names.\n* Methods are ignored.\n\nRequirements\n------------\n* Python 3.7 later\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install call-grph\n\nHistory\n-------\n0.0.1 (2020-4-21)\n~~~~~~~~~~~~~~~~~~\n* first release\n\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/call-graph',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
