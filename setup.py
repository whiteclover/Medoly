#!/usr/bin/env python
# Copyright (C) 2015 Thomas Huang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import medoly


readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(name='medoly',
      version=medoly.__version__,
      description='Medoly is a Web Framework, the design is inspried by Spring-boot and Emberjs.',
      long_description=readme,
      author="Thomas Huang",
      url='https://github.com/whiteclover/medoly',
      author_email='lyanghwy@gmail.com',
      packages=['medoly'],
      install_requires=['setuptools', 'tornado', 'choco'],
      keywords=["Web FrameWork"],
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
