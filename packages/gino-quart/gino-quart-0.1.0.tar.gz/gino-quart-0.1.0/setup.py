# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['gino_quart']
install_requires = \
['gino>=1.0.0rc2,<2.0.0', 'quart>=0.11.5,<0.12.0']

entry_points = \
{'gino.extensions': ['quart = gino_quart']}

setup_kwargs = {
    'name': 'gino-quart',
    'version': '0.1.0',
    'description': 'An extension for GINO to integrate with Quart',
    'long_description': '# gino-quart\n\nAn extension for GINO to support Quart server.\n\n**This project "gino-quart" is currently not maintained and needs adoption.** \n\nSince GINO 1.0, the built-in extensions are now separate projects supported by\nthe community. This project is copied here directly from GINO 0.8.x for\ncompatibility. Help is needed to:\n\n* Keep this project maintained - follow Quart releases, fix issues, etc.\n* Add more examples and documentation.\n* Answer questions in the community.\n',
    'author': 'Tony Wang',
    'author_email': 'wwwjfy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-gino/gino-quart',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
