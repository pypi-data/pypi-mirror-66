# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['gino_tornado']
install_requires = \
['gino>=1.0.0rc2,<2.0.0', 'tornado>=6.0.4,<7.0.0']

entry_points = \
{'gino.extensions': ['tornado = gino_tornado']}

setup_kwargs = {
    'name': 'gino-tornado',
    'version': '0.1.0',
    'description': 'An extension for GINO to integrate with Tornado',
    'long_description': '# gino-tornado\n\nAn extension for GINO to support Tornado server.\n\n**This project "gino-tornado" is currently not maintained and needs adoption.** \n\nSince GINO 1.0, the built-in extensions are now separate projects supported by\nthe community. This project is copied here directly from GINO 0.8.x for\ncompatibility. Help is needed to:\n\n* Keep this project maintained - follow Tornado releases, fix issues, etc.\n* Add more examples and documentation.\n* Answer questions in the community.\n',
    'author': 'Vladimir Goncharov',
    'author_email': 'amatanhead@yandex-team.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-gino/gino-tornado',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5.2,<4.0.0',
}


setup(**setup_kwargs)
