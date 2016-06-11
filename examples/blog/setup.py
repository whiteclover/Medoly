#!/usr/bin/env python

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import blog


readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(name='blog',
      version=blog.__version__,
      description='Blog is simple blog demo wrote by Medoly',
      long_description=readme,
      author="Thomas Huang",
      url='https://github.com/whiteclover/Medoly',
      author_email='lyanghwy@gmail.com',
      packages=['blog'],
      install_requires=['medoly', 'sqlalchemy', 'markdown', 'bcrypt'],
      license="Apache License",
      platforms='any',
      classifiers=(
          "Development Status :: 3 - Alpha",
          "Natural Language :: English",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Operating System :: OS Independent",
      )
      )
