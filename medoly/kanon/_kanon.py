#!/usr/bin/env python

"""Kanon
==========

"""

import os.path

from . import composer

from .manager import InventoryManager


class Kanon(object):
    """Kanon is  medoly application builder

    :param inventory_mgr: the  inventory manager for bootstrap the application
    """

    def __init__(self, inventory_mgr=None):
        self.inventory_mgr = inventory_mgr or InventoryManager.instance()

    @property
    def config(self):
        """Get the application config"""
        return self.inventory_mgr.config

    def chant(self):
        """Initialize the setting and application"""
        return self.inventory_mgr.load()

    def hook(self, point, failsafe=None, priority=None, **kwargs):

        def _hook(func):
            self.inventory_mgr.attach(point, func, failsafe, priority, kwargs)
        return _hook

    def error_page(self, status_code):

        def _error_page(func):
            self.inventory_mgr.error_page(status_code, func)
        return _error_page

    def boot(self):
        def _boot(kclass):
            self.inventory_mgr.put_boot(kclass)
            return kclass
        return _boot

    def set_app_name(self, name):
        self.inventory_mgr.set_app_name(name)

    def set_debug(self):
        from medoly import log
        log.log_config(self.inventory_mgr.app_name, True)

    def compose(self, module, include_template=True):
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
                self.inventory_mgr.add_template_path(tempalte_path)

    def ui(self, template_name=None, name=None):
        def _ui(uicls):
            ui_name = None
            if name and name.strip():
                ui_name = name
            else:
                kclass_name = uicls.__name__
                ui_name = kclass_name

            if template_name is not None:
                uicls.default_template = template_name
            self.inventory_mgr.put_ui(ui_name, uicls)
            return uicls
        return _ui

    def menu(self, url_spec, settings=None, name=None, render=None):
        def __menu(handler):
            self.inventory_mgr.add_route(url_spec, handler, settings, name, render)
            return handler
        return __menu

    def route(self, prefix_url=''):

        def __route(f):
            c = Connetor(prefix_url, self.inventory_mgr)
            f(c)
            return f
        return __route

    def bloom(self, inventory_name, alias=None):
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

                self.inventory_mgr.put_thing(name, inventory)

            elif inventory_name == "model":
                name = None
                if alias and alias.strip():
                    name = alias
                else:
                    name = kclass_name

                self.inventory_mgr.put_model(name, inventory)

            elif inventory_name == "mapper":
                name = None
                if alias and alias.strip():
                    name = alias
                else:
                    if kclass_name.endswith("Mapper"):
                        name = kclass_name[:-6]
                    else:
                        name = kclass_name

                self.inventory_mgr.put_mapper(name, inventory)

            return inventory
        return _bloom


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
        :param args:  the more args for  route
        :param kw: the more settings for route confinguration
        """
        self.mgr.add_menu(self.prefix_path + url_spec, *args, **kw)

    def __exit__(self, exc_type, exc_value, traceback):
        pass
