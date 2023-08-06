#!/usr/bin/env python

import errno
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from raise_ import __doc__, __version__

project_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(project_directory, 'README.rst')

readme_file = open(readme_path)
try:
    long_description = readme_file.read()
finally:
    readme_file.close()

if 'sdist' in sys.argv:
    # When building a source distribution, we need to include the
    # full package with both versions: Python 3 and Python 2.
    kwargs = {'packages': ['raise_']}
else:
    # When not building a source distribution, we can include
    # just the file for the matching Python version.
    kwargs = {'py_modules': ['raise_']}

    packaged_path = os.path.join(project_directory, 'raise_.py')
    if sys.version_info >= (3,):
        source_path = os.path.join(project_directory, 'raise_/raise3.py')
    else:
        source_path = os.path.join(project_directory, 'raise_/raise2.py')
    try:
        os.unlink(packaged_path)
    except OSError as error:
        if error.errno != errno.ENOENT:
            raise
    os.link(source_path, packaged_path)

setup(
    name='raise',
    version=__version__ + '.post2',
    description=__doc__.split('\n')[0],
    long_description=long_description,
    license='0BSD',
    url='https://github.com/mentalisttraceur/python-raise',
    author='Alexander Kozhevnikov',
    author_email='mentalisttraceur@gmail.com',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],
    **kwargs
)
