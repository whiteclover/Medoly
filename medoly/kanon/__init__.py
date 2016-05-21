#!/usr./bin/env python


"""Kanon
=========
"""

import os.path

from .manager import InventoryManager
from . import composer


def chant():
    """Initialize the setting and application"""
    return InventoryManager.instance().load()


def hook(point, failsafe=None, priority=None, **kwargs):

    def _hook(func):
        InventoryManager.instance().attach(point, func, failsafe, priority, kwargs)
    return _hook


def error_page(status_code):

    def _error_page(func):
        InventoryManager.instance().error_page(status_code, func)
    return _error_page


def boot():
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


def compose(module, include_template=True):
    """Scan the module including all sub modules. 
    check the template path ``template``, if exists, will add it in the template engine paths

    :param module: the python dot module string.
    :param include_template: if the module is a diretory and the value is true. it will add the template path,
            if exist the sub diretory named "template".
    """
    module_infso, is_path, package = composer.scan_submodules(module)
    if is_path and include_template:
        path = os.path.dirname(package.__file__)
        tempalte_path = os.path.join(path, "template")
        if os.path.isdir(tempalte_path):
            InventoryManager.instance().add_template_path(tempalte_path)


def ui(template_name=None, name=None):
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


def menu(url_spec, settings=None, name=None, render=None):
    def __menu(handler):
        InventoryManager.instance().add_route(url_spec, handler, settings, name, render)
        return handler
    return __menu


def route(prefix_url=''):

    def __route(f):
        c = composer.Connetor(prefix_url, InventoryManager.instance())
        f(c)
        return f
    return __route


def bloom(inventory_name, alias=None):
    """Bind the inventory"""
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
