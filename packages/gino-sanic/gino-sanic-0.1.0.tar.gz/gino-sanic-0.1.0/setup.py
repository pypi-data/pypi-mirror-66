# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['gino_sanic']
install_requires = \
['gino>=1.0.0rc2,<2.0.0', 'sanic>=19.12.2,<20.0.0']

entry_points = \
{'gino.extensions': ['sanic = gino_sanic']}

setup_kwargs = {
    'name': 'gino-sanic',
    'version': '0.1.0',
    'description': 'An extension for GINO to integrate with Sanic',
    'long_description': '# gino-sanic\n\nAn extension for GINO to support Sanic server.\n\n**This project "gino-sanic" is currently not maintained and needs adoption.** \n\nSince GINO 1.0, the built-in extensions are now separate projects supported by\nthe community. This project is copied here directly from GINO 0.8.x for\ncompatibility. Help is needed to:\n\n* Keep this project maintained - follow Sanic releases, fix issues, etc.\n* Add more examples and documentation.\n* Answer questions in the community.\n',
    'author': 'Samuel Li',
    'author_email': 'lbhsot@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-gino/gino-sanic',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
