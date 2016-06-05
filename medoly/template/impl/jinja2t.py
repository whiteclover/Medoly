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

"""Jinaj2 Template Loader"""

from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache
import jinja2


# Fixed template render
jinja2.Template.generate = jinja2.Template.render


class Jinja2Loader(object):
    """Implementing customized Template Loader of for tornado to generate jinja2 template

    :param directories: the template paths
    :type directories: lst[string]
    :param kwargs: the more settings for jinja2 environment.
    :type kwargs: dict
    :param cache_path: the jinja2 btye cache path, defaults to cache
    :type cache_path: string, optional
    :param cache_size: the byte cache collection size, defaults to -1
    :type cache_size: number, optional
    :param auto_reload: Refresh the template when template modified, defaults to False not reload the template.
    :type auto_reload: bool, optional
    :param autoescape: enable the escape for row text, defaults to True
    :type autoescape: bool, optional
    """

    def __init__(self, directories, cache_path=None, cache_size=-1, auto_reload=False, autoescape=True, **kwargs):

        bcc = None
        if cache_path:
            # if not os.path.exists(cache_path):
            #     os.makedirs(cache_path)
            bcc = FileSystemBytecodeCache(directory=cache_path)
        self.env = Environment(loader=FileSystemLoader(directories), bytecode_cache=bcc,
                               auto_reload=auto_reload,
                               cache_size=cache_size,
                               autoescape=autoescape,
                               ** kwargs)

    def load(self, name, parent_path=None):
        """Load the template by name"""
        return self._create_template(name)

    def _create_template(self, name):
        return self.env.get_template(name)

    def reset(self):
        """Reset the template cache collection"""
        if hasattr(self.env, 'bytecode_cache') and self.env.bytecode_cache:
            self.env.bytecode_cache.clear()
