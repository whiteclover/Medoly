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


"""Mako Tempatle Engine

Example
--------------

index.html:

.. code::

    <p>This is an UI Page</p>


.. code:: python

    t = lookup.TemplateLookup(directories=["template"])
    t.get_template("index.html").render(post_id=122)

"""

from mako.lookup import TemplateLookup
from mako.template import Template

# Fixed template render
Template.generate = Template.render


class MakoLoader(object):
    """Mako Tempatle Engine Loader

    :param  list[str] directories: the Mako template root paths
    :param  kwargs: the more settings for Mako template

    :param string module_directory: the Mako template module cache path (default: {None})
    :param bool filesystem_checks: when ``True`` the Mako loader will check the template file and reload the last modify template(default: {False})

    """

    def __init__(self, directories, module_directory=None, filesystem_checks=False, **kwargs):
        self._lookup = TemplateLookup(directories=directories,
                                      filesystem_checks=filesystem_checks,
                                      module_directory=module_directory,
                                      input_encoding='utf-8',
                                      output_encoding='utf-8',
                                      default_filters=['decode.utf8'],
                                      **kwargs)

    def load(self, name, parent_path=None):
        """Load the template by name"""
        return self._create_template(name)

    def _create_template(self, name):
        """The tornado temaple loader load the real tempalte


        :param name: the template path name
        :type name:  string
        :returns: the Mako template instance
        :rtype: {Template}
        """
        template = self._lookup.get_template(name)

        return template

    def reset(self):
        pass
