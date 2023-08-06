#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import setup

# read the contents of your README file
this_directory = Path(__file__).parent.resolve()
long_description = Path(this_directory, 'README.md').read_text()

version = 'v1.4'

setup(
    name='procamora-utils',  # How you named your package folder (MyLib)
    packages=['procamora_utils'],  # Chose the same as "name"
    version=version[1:],  # Start with a small number and increase it with every change you make
    license='gpl-3.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='This repository contains a set of libraries that i use in other projects',
    # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='procamora',  # Type in your name
    author_email='pablojoserocamora@gmail.com',  # Type in your E-Mail
    url='https://github.com/procamora/python3-utils',  # Provide either the link to your github or to your website
    download_url=f'https://github.com/procamora/python3-utils/archive/{version}.tar.gz',  # I explain this later on
    keywords=['sqlite', 'sql', 'sqlite3', 'network', 'fqdn', 'ip', 'ipv4', 'ipv6', 'icmp', 'ping', 'logging', 'color',
              'log'],
    # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'colorlog',
    ],
    classifiers=[  # https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: System :: Logging',
        'Topic :: Database',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # Again, pick a license
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    # py_modules=["interface_sqlite"],  # Required
    python_requires='<4, >=3.5',
)
