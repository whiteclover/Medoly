import os.path

from .manager import InventoryManager

from functools import wraps
from . import composer
__inventoryMgr = InventoryManager()


def boot():
    pass


def set_app_name(name):
    __inventoryMgr.set_app_name(name)


def set_debug():
    from medoly import log
    log.log_config(__inventoryMgr.app_name, True)


def inventory_mgr():
    return __inventoryMgr


def compose(module, include_template=True):
    module_infso, is_path, package = composer.import_submodules(module)

    if is_path and include_template:
        path = os.path.dirname(package.__file__)
        tempalte_path = os.path.join(path, "template")
        if os.path.isdir(tempalte_path):
            __inventoryMgr.add_template_path(tempalte_path)


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
        __inventoryMgr.put_ui(ui_name, uicls)
        return uicls
    return _ui


def menu(url_spec, settings=None, name=None, render=None):
    def __menu(handler):
        __inventoryMgr.add_route(url_spec, handler, settings, name, render)
        return handler
    return __menu


def route(prefix_url=''):

    def __def(f):
        c = Connetor(prefix_url, __inventoryMgr)
        f(c)
        return f
    return __def


def chant():
    return __inventoryMgr.load()


def bloom(inventory_name, alias=None):

    def _bloom(inventory):
        kclass_name = inventory.__name__
        if inventory_name == "thing":
            name = None
            if alias and alias.strip():
                name = alias
            else:
                if kclass_name.endswith("Thing"):
                    name = kclass_name[:4]
                else:
                    name = kclass_name

            __inventoryMgr.put_thing(name, inventory)

        elif inventory_name == "model":
            name = None
            if alias and alias.strip():
                name = alias
            else:
                name = kclass_name

            __inventoryMgr.put_model(name, inventory)

        elif inventory_name == "mapper":
            name = None
            if alias and alias.strip():
                name = alias
            else:
                if kclass_name.endswith("Mapper"):
                    name = kclass_name[:4]
                else:
                    name = kclass_name

            __inventoryMgr.put_mapper(name, inventory)

        return inventory
    return _bloom


class Connetor(object):

    def __init__(self, prefix_path, mgr):
        self.prefix_path = prefix_path
        self.mgr = mgr

    def __enter__(self):
        return self

    def connect(self,  url_spec, *args, **kw):
        self.autoload.add_menu(self.prefix_path + url_spec, *args, **kw)

    def __exit__(self, exc_type, exc_value, traceback):
        pass
