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

import importlib
import pkgutil

import logging

LOGGER = logging.getLogger("kanon.composer")


def scan_submodules(package, recursive=True):
    """Import and scan all submodules of a module, recursively, including sub packages,

    :param package: package (name or actual module)
    :type package: str | module
    :returns: the  package infos, is a path module info, and the current package module instance
    :rtype: (dict[str, types.ModuleType], bool, top level module)
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    package_infos = {}
    is_path = False
    if hasattr(package, "__path__"):
        is_path = True
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            package_infos[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                LOGGER.debug("Scaning package: %s", full_name)
                package_infos.update(scan_submodules(full_name)[0])
    return package_infos, is_path, package


class Connector(object):
    """Route menu processor

    :param url_prefix: the url route path prefix
    :type url_prefix: string
    :param mgr: the inventory manager for adding routes
    :type mgr:  InventoryManager
    """

    def __init__(self, url_prefix, mgr):

        self.url_prefix = url_prefix
        self.mgr = mgr

    def __enter__(self):
        return self

    def connect(self, url_spec, handler=None, setting=None, name=None, render=None):
        """Added a url route handler

        If  ``render`` is not ``None``, it will use the template render hanlder, else use the ``handler`` as request handler class.

        :param url_spec:  the url path
        :type url_spec: string
        :param handler: the tornado web request handler class, defaults to None
        :type handler: the subclass of WebRequestHandler,  optional
        :param settings: the handler setting config, defaults to None
        :type settings: dict, optional
        :param name: the name for reverse url, defaults to None
        :type name: string, optional
        :param render: the temaplate path for tempalte render handler, defaults to None
        :type render: string, optional
        """
        self.mgr.add_route(self.url_prefix + url_spec, handler, setting, name, render)

    def __exit__(self, exc_type, exc_value, traceback):
        self.mgr = None
