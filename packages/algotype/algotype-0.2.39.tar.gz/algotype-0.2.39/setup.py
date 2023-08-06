# -*- coding: utf-8 -*-
 
'''
setup.py: setuptools control.
'''

from setuptools import setup
import algotype.meta as meta

# read the contents of the README file
import os
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as fh:
    long_description = fh.read()

setup_data = {
    'name': 'algotype',
    'packages':  ['algotype'],
    'entry_points':  {
        'console_scripts': ['algotype = algotype.algotype:main']
        },
    'version':  meta.version,
    'description':  meta.description,
    'long_description': long_description,
    'long_description_content_type': 'text/x-rst',
    'author':  meta.author,
    'author_email':  meta.author_email,
    'maintainer': meta.maintainer,
    'maintainer_email': meta.maintainer_email,
    'url':  'http://algotype.org',
    'classifiers': [
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        # 'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        # ~ 'Programming Language :: Python :: 3.6',
        # ~ 'Programming Language :: Python :: 3.7',
        # ~ 'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    'python_requires': '>=3.6',

}

setup(**setup_data)

# ~ setup(
    # ~ name = "algotype",
    # ~ packages = ["algotype"],
    # ~ entry_points = {
        # ~ "console_scripts": ['algotype = algotype.algotype:main']
        # ~ },
    # ~ version = meta.version,
    # ~ description = meta.description,
    # ~ author = meta.author,
    # ~ author_email = meta.author_email,
    # ~ url = "http://algotype.org",
    # ~ )