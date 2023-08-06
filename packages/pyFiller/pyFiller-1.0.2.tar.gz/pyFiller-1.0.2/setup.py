#!/usr/bin/env python

"""

"""

from os import path
from setuptools import setup
from pyfiller import __config__ as config


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

console_scripts = []
for src_basename in config.CONSOLE_SCRIPTS:
    details = config.CONSOLE_SCRIPTS[src_basename]
    console_scripts.append('{}={}.{}:main'.format(details['scriptname'], details['path'], src_basename))
print(console_scripts)

setup(
    name=config.PKGNAME,
    version=config.VERSION,
    description=config.DESCRIPTION,
    author='Martin F. Falatic',
    author_email='martin@falatic.com',
    license='MIT License',
    keywords='filesystem wipe filler generator',
    url='https://github.com/MartinFalatic/pyfiller',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 5 - Production/Stable',
    ],
    packages=[
        'pyfiller',
    ],
    entry_points={
        'console_scripts': console_scripts,
    },
    install_requires=[
        'colorama',
        'humanfriendly',
        'tqdm',
    ],
    extras_require={},
    package_data={},
    data_files=[],
    # Derived data
    long_description=long_description,
    long_description_content_type='text/markdown',
)
