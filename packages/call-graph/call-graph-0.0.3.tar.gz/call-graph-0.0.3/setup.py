# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['call_graph']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.2.0,<9.0.0']

entry_points = \
{'console_scripts': ['call-graph = call_graph:main']}

setup_kwargs = {
    'name': 'call-graph',
    'version': '0.0.3',
    'description': '`call-graph` is a package for viewing call graph.',
    'long_description': '`call-graph` is a package for viewing call graph.\n::\n\n   $ call-graph\n   usage: call-graph [-h] [-p PATH] [-u] [-o] [-n NO_TARGET] module func\n   call-graph: error: the following arguments are required: module, func\n   \n   $ call-graph call_graph main\n   main\n   ├ get_names\n   ├ get_call_graph\n   └ call_graph_view\n\n* "NO_TARGET" is used for ignoring names.\n* Methods are ignored.\n* Use `_ = function` for dummy call.\n\nRequirements\n------------\n* Python 3.8 later, more-itertools\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install call-graph\n\nHistory\n-------\n0.0.1 (2020-4-21)\n~~~~~~~~~~~~~~~~~~\n* first release\n\n',
    'author': 'SaitoTsutomu',
    'author_email': 'tsutomu7@hotmail.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/call-graph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
