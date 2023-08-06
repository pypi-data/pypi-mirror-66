# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['macrobot_paper']
entry_points = \
{'console_scripts': ['mb = macrobot_paper:main']}

setup_kwargs = {
    'name': 'macrobot-paper',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
