# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['runtime_syspath']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'runtime-syspath',
    'version': '0.1.0',
    'description': "Function to find each 'src' directory under working directory and add it to sys.path.",
    'long_description': None,
    'author': 'Greg Kedge',
    'author_email': 'gregwork@kedges.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
