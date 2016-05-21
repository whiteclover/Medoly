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
    """ Import and scan all submodules of a module, recursively, including sub packages, 

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    is_path = False
    if hasattr(package, "__path__"):
        is_path = True
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                LOGGER.debug("Scaning package: %s", full_name)
                results.update(scan_submodules(full_name)[0])
    return results, is_path, package


class Connetor(object):
    """Route menu processor

        :param prefix_path: the url route path prefix
        :type prefix_path: stirng
        :param mgr: the inventory manager for adding routes
        :type mgr:  InventoryManager
    """

    def __init__(self, prefix_path, mgr):

        self.prefix_path = prefix_path
        self.mgr = mgr

    def __enter__(self):
        return self

    def connect(self, url_spec, *args, **kw):
        """Added a url route handler

        :param url_spec: the url path or URLSpec
        :type url_spec: string|url
        :param args:  the more args for  route
        :param kw: the more settings for route confinguration
        """
        self.mgr.add_menu(self.prefix_path + url_spec, *args, **kw)

    def __exit__(self, exc_type, exc_value, traceback):
        pass
