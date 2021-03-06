#!/usr/bin/env python
#
# Copyright 2016 Medoly
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import os

from setuptools import setup, find_packages

import medoly


readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(name='medoly',
      version=medoly.__version__,
      description='Medoly is a Web Framework, the design is inspried by Spring-boot and Emberjs.',
      long_description=readme,
      author="Thomas Huang",
      url='https://github.com/whiteclover/medoly',
      author_email='lyanghwy@gmail.com',
      packages=find_packages(exclude=["t"]),
      install_requires=['setuptools', 'tornado', 'jinja2', 'mako'],
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
