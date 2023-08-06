#!/usr/bin/env python
#
# GeoTiler - library to create maps using tiles from a map provider
#
# Copyright (C) 2014-2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice (restored, based on setup.py file from
# https://github.com/stamen/modestmaps-py):
#
#   Copyright (C) 2007-2013 by Michal Migurski and other contributors
#   License: BSD
#

import ast
from setuptools import setup, find_packages

VERSION = ast.parse(
    next(l for l in open('geotiler/__init__.py') if l.startswith('__version__'))
).body[0].value.s

setup(
    name='geotiler',
    packages=find_packages('.'),
    include_package_data=True,
    scripts=('bin/geotiler-lint', 'bin/geotiler-route', 'bin/geotiler-fetch'),
    version=VERSION,
    description='GeoTiler - library to create maps using tiles'
        ' from a map provider',
    author='Artur Wroblewski',
    author_email='wrobell@riseup.net',
    url='https://wrobell.dcmod.org/geotiler/',
    project_urls={
        'Code': 'https://github.com/wrobell/geotiler',
        'Issue tracker': 'https://github.com/wrobell/geotiler/issues',
    },
    setup_requires = ['setuptools_git >= 1.0'],
    install_requires=['Pillow', 'cytoolz >= 0.8.2', 'aiohttp >= 2.3.5'],
    classifiers=[
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 4 - Beta',
    ],
    long_description=open('README').read(),
    long_description_content_type='text/x-rst',
    license='GPL (includes BSD licensed code)',
)

# vim: sw=4:et:ai
