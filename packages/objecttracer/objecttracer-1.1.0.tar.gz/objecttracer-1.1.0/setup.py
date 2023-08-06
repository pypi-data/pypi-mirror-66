# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['objecttracer']
setup_kwargs = {
    'name': 'objecttracer',
    'version': '1.1.0',
    'description': 'Small utility to log the activity on a given object.',
    'long_description': None,
    'author': 'Sylvain Roy',
    'author_email': 'sylvain.roy@m4x.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
