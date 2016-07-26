#!/usr/bin/env python
"""
Universe Release Versioning - Python Implementation

Author: Alpha <alpha@alphaservcomputing.solutions>
"""

import re
import subprocess

from setuptools import setup, find_packages

with open('requirements.txt') as req_file:
    requirements = []
    for line in req_file:
        if '#' in line:
            line, comment_ = line.split('#', 1)
        line = line.strip()
        if line:
            requirements.append(line)


__version__ = '0.1.0'  # Overwritten below
with open('universe/version.py') as handle:
    exec(handle.read())  # pylint: disable=exec-used

if '$Id:' in __version__:
    # Replace the smudged $Id:<sha1>$ with <sha1>
    __version__ = re.sub(r'\$Id:([^$]+)\$', r'\1', __version__)
elif '$Id$' in __version__:
    # Replace non-smudged $Id$ with <sha1>
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    __version__ = __version__.replace('$Id$', sha)

setup(
    name='universe',
    version=__version__,
    description='Universe Release Versioning',
    url='https://github.com/Alphadelta14/universe',
    author='Alphadelta14',
    author_email='alpha@alphaservcomputing.solutions',
    license='MIT License',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'universe-clean = universe.gitfilter:clean',
            'universe-init = universe.gitfilter:main',
            'universe-smudge = universe.gitfilter:smudge',
            'universe-release = universe.release:main',
        ],
        'distutils.commands': [
            'release = universe.release:dev',
            'major_release = universe.release:major',
            'minor_release = universe.release:minor',
            'patch_release = universe.release:patch',
        ]
    },
    scripts=[
        'bin/universe-clean',
        'bin/universe-init',
        'bin/universe-smudge',
    ],
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Version Control',
        'Topic :: Utilities',
    ]
)
