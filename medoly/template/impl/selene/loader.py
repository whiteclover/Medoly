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
import stat
import posixpath
import re

try:
    import threading
except:
    import dummy_threading as threading


from . import errors

from mako import util
from tornado.template import Template, _DEFAULT_AUTOESCAPE


class SeleneLoader(object):
    """The Selene Template Loader

     :param directories: the  template root paths
    :type directories: lst[string]
    :param filesystem_checks: the ui template container (default: {None})
    :type filesystem_checks: bool, optional
    :param collection_size: the collection template  size, defaults to -1  no limit size.
    :type collection_size: number, optional
    :param UIContainer ui_container: when ``True`` the  loader will check the template file
            and reload the last modify template(default: {False})
    :param string autoescape: The name of a function in the template namespace, such
            as "xhtml_escape", or ``None`` to disable autoescaping by default.
    :param dict namespace: A dictionary to be added to the default template
            namespace, or ``None``.
    :param string whitespace: A string specifying default behavior for
            whitespace in templates; see `filter_whitespace` for options.
            Default is "single" for files ending in ".html" and ".js" and
            "all" for other files.
    """

    def __init__(self, directories, ui_container=None, filesystem_checks=True, collection_size=-1,
                 autoescape=_DEFAULT_AUTOESCAPE, namespace=None, whitespace=None):
        self.directories = [posixpath.normpath(d) for d in
                            util.to_list(directories, ())
                            ]

        self.autoescape = autoescape
        self.namespace = namespace or {}
        self.whitespace = whitespace
        self.templates = {}
        self.filesystem_checks = filesystem_checks
        self.collection_size = collection_size
        self.ui_container = ui_container
        if self.ui_container:
            self.ui_container.set_loader(self)

        #: the basic template namespace
        self.namespace.update({
            "_loader": self,
            "handler": None,
            "__ttmodule": ui_render})

        if collection_size == -1:
            self.collection = {}
            self._uri_cache = {}
        else:
            self.collection = util.LRUCache(collection_size)
            self._uri_cache = util.LRUCache(collection_size)
        self._mutex = threading.Lock()

    def get_ui(self, ui_name):
        return self.ui_container.get_ui(ui_name)

    def reset(self):
        """Resets the cache of compiled templates."""
        pass

    def load(self, uri, parent_path=None):
        """Return a : class: `.Template` object corresponding to the given
        ``uri``.

        .. note:: The ``relativeto`` argument is not supported here at
           the moment.
        """

        try:
            if self.filesystem_checks:
                return self.check(uri, self.collection[uri])
            else:
                return self.collection[uri]
        except KeyError:
            u = re.sub(r'^\/+', '', uri)
            for directory in self.directories:
                # make sure the path seperators are posix - os.altsep is empty
                # on POSIX and cannot be used.
                directory = directory.replace(os.path.sep, posixpath.sep)
                srcfile = posixpath.normpath(posixpath.join(directory, u))
                if os.path.isfile(srcfile):
                    return self._create_template(srcfile, uri)
            else:
                raise errors.TopLevelLoaderException(
                    "Cant locate template for uri %r" % uri)

    def _create_template(self, filename, uri):
        self._mutex.acquire()
        try:
            try:
                # try returning from collection one
                # more time in case concurrent thread already loaded
                return self.collection[uri]
            except KeyError:
                pass
            try:
                with open(filename, "rb") as f:
                    self.collection[uri] = template = Template(f.read(), name=posixpath.normpath(filename), loader=self)
                    template_stat = os.stat(filename)
                    template._modified_time = template_stat[stat.ST_ATIME]
                    return template
            except:
                # if compilation fails etc, ensure
                # template is removed from collection,
                # re-raise
                self.collection.pop(uri, None)
                raise
        finally:
            self._mutex.release()

    def check(self, uri, template):
        """Check the template modified, and refresh to latest version

        : param uri: the template path uri
        : type uri: string
        : param template: the template instance
        : returns: the template instance
        : raises: errors
        """
        try:
            template_stat = os.stat(template.name)
            if template._modified_time < template_stat[stat.ST_MTIME]:
                self.collection.pop(uri, None)
                return self._create_template(template.name, uri)
            else:
                return template
        except OSError:
            self.collection.pop(uri, None)
            raise errors.TemplateLoaderException(
                "Cant locate template for uri %r" % uri)


def ui_render(loader, handler, name, *args, **kw):
    """Ui render"""
    uicls = loader.get_ui(name)
    ui = uicls(handler, loader)
    return ui._execute(*args, **kw)
