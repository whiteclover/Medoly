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

import re
import os
import posixpath

from mako import util

from . import errors


class UIModule(object):
    """UIModule for selene template module expression


    :param handler: The current request handler, the subclass of RequestHandler.
    :param loader: The template loader
    :param template: The template path for ui render, Defaults using default_template.
    :type template: string, optional
    :raises: UINestedCallException, when nested call ui in module render.
    """

    default_template = "index.html"
    """Default template for render module"""

    def __init__(self, handler, loader, template=None):
        self.loader = loader
        self.ui_container = self.loader.ui_container
        self.template = template or self.default_template
        if handler is None:
            raise errors.UINestedCallException("Cant call an ui module in an ui module template: {}".format(self.template))
        self.handler = handler
        self.initialize()

    @property
    def current_user(self):
        """Get current handler user"""
        return self.handler.current_user

    def initialize(self):
        """Initialize the setting before render

        Implements it in subclass to hook initialize settings.
        """
        pass

    def _execute(self, *args, **kw):
        """Execute and render the template"""
        data = self.render(*args, **kw)
        t = self.get_template()

        return t.generate(**data)

    def get_template(self):
        """Gets the template"""
        return self.ui_container.get_template(self.template)

    def render(self, *args, **kw):
        """Entry point and logic section for custom appliction actions"""
        raise NotImplementedError("Must implement in subclass")


class UIContainer(object):

    def __init__(self, ui_paths, uis=None):
        """Init ui container,

        param ui_paths: the ui template paths.
        param uis: the dict like object, contains the  ui module classes.
        """
        self.ui_paths = [posixpath.normpath(d) for d in
                         util.to_list(ui_paths, ())
                         ]
        self.uis = uis or dict()
        self.loader = None

    def put_ui(self, ui_name, uicls):
        """Add a ui"""
        self.uis[ui_name] = uicls

    def get_ui(self, ui_name):
        """Get a ui by name"""
        uicls = self.uis.get(ui_name)
        if uicls is None:
            raise errors.UINotFoundException("Cant find ui for %s" % ui_name)
        return uicls

    def set_loader(self, loader):
        """Set up template loader"""
        self.loader = loader

    def get_template(self, uri):
        """Return a :class:`.Template` object corresponding to the given
            ``uri``.

            .. note:: The ``relativeto`` argument is not supported here at
               the moment.
        """
        # the spefical ui uri with prefix "url#"
        uiuri = "ui#" + uri
        try:
            if self.loader.filesystem_checks:
                return self.loader.check(uiuri, self.loader.collection[uiuri])
            else:
                return self.loader.collection[uiuri]
        except KeyError:
            u = re.sub(r'^\/+', '', uri)
            for directory in self.ui_paths:
                # make sure the path seperators are posix - os.altsep is empty
                # on POSIX and cannot be used.
                directory = directory.replace(os.path.sep, posixpath.sep)
                srcfile = posixpath.normpath(posixpath.join(directory, u))
                if os.path.isfile(srcfile):
                    return self.loader._create_template(srcfile, uiuri)
                else:
                    raise errors.TopLevelLoaderException(
                        "Cant locate ui template for uri %r" % uiuri)
