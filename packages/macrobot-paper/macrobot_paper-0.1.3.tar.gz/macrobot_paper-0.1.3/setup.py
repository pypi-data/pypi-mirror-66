# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['macrobot_paper']
install_requires = \
['numpy>=1.18.3,<2.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'scikit-image>=0.16.2,<0.17.0']

entry_points = \
{'console_scripts': ['mb = run_pipeline:main']}

setup_kwargs = {
    'name': 'macrobot-paper',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Stefanie Lueck',
    'author_email': 'lueck@ipk-gatersleben.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
