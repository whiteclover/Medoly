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


"""Kanon
=========
"""

import os.path

from .manager import InventoryManager
from . import composer
from ._kanon import Melos


def chant():
    """Initialize the setting and application"""
    return InventoryManager.instance().load()


def hook(point, failsafe=None, priority=None, **kwargs):
    """Add a hook point for application"""

    def _hook(func):
        InventoryManager.instance().attach(point, func, failsafe, priority, kwargs)
    return _hook


def error_page(status_code):
    """Add an error page handler for the application"""

    def _error_page(func):
        InventoryManager.instance().error_page(status_code, func)
    return _error_page


def boot():
    """Add a boot config or boot configs

    Examples:

    .. code-block:: python

        # add a config class
        @kanon.boot()
        class SiteConfig(object):
            def config(self, options):
                group = options.group("Service settings")
                _ = group.define
                _('-H', '--server.host', default='localhost', help='The host of the http server (default %(default)r)')

        # add a more than one boot config class at once
        @kanon.boot()
        def boots():
            return [BlalaConfig, DemoConfig]
    """
    def _boot(kclass):
        InventoryManager.instance().put_boot(kclass)
        return kclass
    return _boot


def set_app_name(name):
    InventoryManager.instance().set_app_name(name)


def set_debug():
    from medoly import log
    log.log_config(InventoryManager.instance().app_name, True)


def inventory_manager():
    """Get the current kanon inventory manager"""
    return InventoryManager.instance()


def compose(module, url_prefix="", template_path="template"):
    """Scan the module including all sub modules.

    Checks the template path , if exists, will add it in the template engine paths.

    :param module: the python dot module string.
    :param string url_prefix: sets the current package url prefix for url route.
    :param template_path: if the module is a diretory and set the template path. it will add the template path,
            if exists the subdiretory  ``template_path`` in the current scan module directory. Defaults to "template".
    """
    # settings to current url prefix
    InventoryManager.instance().compose_url_prefix = url_prefix
    module_infso, is_path, package = composer.scan_submodules(module)
    if is_path and template_path:
        path = os.path.dirname(package.__file__)
        full_template_path = os.path.join(path, template_path)
        if os.path.isdir(full_template_path):
            InventoryManager.instance().add_template_path(full_template_path)


def ui(template_name, name=None):
    """Adds a ui module hanlder in manager


    :param template_name: the ui  cutom  template path.
    :type template_name: string
    :param name: the name for template engine calling, defaults to  ui class name.
    :type name: string, optional
    """

    def _ui(uicls):
        ui_name = None
        if name and name.strip():
            ui_name = name
        else:
            kclass_name = uicls.__name__
            ui_name = kclass_name

        if template_name is not None:
            uicls.default_template = template_name
        InventoryManager.instance().put_ui(ui_name, uicls)
        return uicls
    return _ui


def menu(url_spec, settings=None, name=None):
    """Adds a url route in manager"""
    def __menu(handler):
        InventoryManager.instance().add_route(url_spec, handler, settings, name)
        return handler
    return __menu


def route(prefix_url=''):
    """Uses connector to add route in manager"""

    def __route(f):
        c = composer.Connetor(prefix_url, InventoryManager.instance())
        f(c)
        return f
    return __route


def bloom(inventory_name, alias=None):
    """Binds the inventory"""

    # check the inventory name validation
    if inventory_name not in ['model', 'thing', 'mapper']:
        raise KeyError("Kanon doesn't have the inventory stragery for ``{}``".format(inventory_name))

    def _bloom(inventory):
        kclass_name = inventory.__name__
        if inventory_name == "thing":
            name = None
            if alias and alias.strip():
                name = alias
            else:
                if kclass_name.endswith("Thing"):
                    name = kclass_name[:-5]
                else:
                    name = kclass_name

            InventoryManager.instance().put_thing(name, inventory)

        elif inventory_name == "model":
            name = None
            if alias and alias.strip():
                name = alias
            else:
                name = kclass_name

            InventoryManager.instance().put_model(name, inventory)

        elif inventory_name == "mapper":
            name = None
            if alias and alias.strip():
                name = alias
            else:
                if kclass_name.endswith("Mapper"):
                    name = kclass_name[:-6]
                else:
                    name = kclass_name

            InventoryManager.instance().put_mapper(name, inventory)

        return inventory
    return _bloom


def chord(name=None, **settings):
    """Adds a chord"""

    def _chord(inventory):
        kclass_name = inventory.__name__
        if name and name.strip():
            kclass_name = name.strip()
        InventoryManager.instance().put_chord(kclass_name, inventory, **settings)
        return inventory
    return _chord
