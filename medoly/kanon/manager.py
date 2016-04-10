import os.path
import re
import logging
from medoly import anthem


from .ctx import AppContext
from choco.ui import UIContainer, UIModule


LOGGER = logging.getLogger("kanon.manager")


class InventoryManager(object):

    def __init__(self, handlercls=None):
        self.boots = []
        self.app_ctx = AppContext()
        self.models = {}
        self.things = {}
        self.routes = []
        self.menus = []
        self.app_name = "Medoly"

        self.mappers = {}
        self.defalut_handler = handlercls or anthem.Handler
        self.template_mananger = TempateMananger()

    def set_app_name(self, name):
        self.app_name = name

    def load(self):
        self.mount_model()
        self.mount_mapper()
        self.mount_thing()
        self.mount_menu()
        return self.create_app()

    def create_app(self):
        LOGGER.debug("Creating app!")
        settings = self.intitilaize_app_settings()
        return anthem.Application(self.routes, self.initilaize_app, **settings)

    def initilaize_app(self, app):
        LOGGER.debug("Starting init app!")
        LOGGER.debug("Start init app hooks!")
        for hook in self.app_ctx.hooks:
            app.attach(*hook[0], **hook[1])

    def intitilaize_app_settings(self):
        settings = dict()
        # try bind template loader
        if self.template_mananger.is_valid():
            LOGGER.debug("Init template!")
            settings[
                'template_loader'] = self.template_mananger.create_template_loader(self)

        return settings

    def put_ui(self, ui_name, uicls):
        if not issubclass(uicls, UIModule):
            classes = [UIModule] + list(uicls.__bases__)
            uicls = type(uicls.__name__, tuple(classes), dict(uicls.__dict__))

        LOGGER.debug("Putting ui:<%s -> %r", ui_name, uicls)
        self.template_mananger.put_ui(ui_name, uicls)

    def put_model(self, name, model):
        LOGGER.debug("Puting model:<%s -> %r", name, model)
        self.models[name] = model

    def put_mapper(self, name, mapper):
        LOGGER.debug("Puting mapper:<%s -> %r", name, mapper)
        self.mappers[name] = mapper

    def put_thing(self, name, thing):
        LOGGER.debug("Puting thing:<%s -> %r", name, thing)
        self.things[name] = thing

    def add_template_path(self, template_path):
        LOGGER.debug("Adding template path: '%s'", template_path)
        self.template_mananger.add_template_path(template_path)
        ui_path = os.path.join(template_path, "ui")
        if os.path.isdir(ui_path):
            LOGGER.debug("Adding template ui path : '%s'", ui_path)
            self.template_mananger.add_ui_path(ui_path)

    def add_route(self, url_spec, handler=None, settings=None, name=None, render=None):
        self.menus.append(Menu(url_spec, handler, settings, name, render))

    def mount_model(self):
        setattr(anthem.handler, '__model', self.models)

    def mount_mapper(self):
        mappers = {}
        for mapper_name in self.mappers:
            mapper = self.mappers.get(mapper_name)
            mappers[mapper_name] = mapper()

        self.mappers = mappers
        setattr(anthem.handler, '__backend', mappers)

    def mount_thing(self):
        things = {}
        for thing_name in self.things:
            thing = self.things.get(thing_name)
            things[thing_name] = thing()

        self.things = things
        setattr(anthem.handler, '__thing', things)

    def mount_menu(self):
        for menu in self.menus:
            self.connect(menu.url_spec, menu.handler,
                         menu.settings, menu.name, menu.render)

    def connect(self, url_spec, handler=None, settings=None, name=None, render=None):

        if render:
            self.routes.append(
                (url_spec, anthem.RenderHandler, dict(template=render)))
            return

        if handler is None:
            raise ValueError("Handler is required, can't be empty")

        self.load_mapper(handler)
        self.load_thing(handler)

        if not issubclass(handler, self.defalut_handler):
            classes = [self.defalut_handler] + list(handler.__bases__)
            handler = type(handler.__name__, tuple(
                classes), dict(handler.__dict__))

        self.routes.append(anthem.url(url_spec, handler, settings, name))

    def load_mapper(self, handler):
        REG = re.compile(r"(\w[\w\d_]+)\s*\-\s*>\s*(\w[\w\d_]+)")
        doc = getattr(handler,  '__mapper__', "")
        if doc:
            lines = [part.strip() for part in doc.split("\n") if part.strip()]
            for line in lines:
                match = REG.match(line)
                if match:
                    name, model_name = match.group(1), match.group(2)
                    setattr(handler, name, self.mappers[model_name])

            delattr(handler, '__mapper__')

    def load_thing(self, handler):
        REG = re.compile(r"(\w[\w\d_]+)\s*\-\s*>\s*(\w[\w\d_]+)")
        doc = getattr(handler,  '__thing__', "")
        if doc:
            lines = [part.strip() for part in doc.split("\n") if part.strip()]
            for line in lines:
                match = REG.match(line)
                if match:
                    name, model_name = match.group(1), match.group(2)
                    setattr(handler, name, self.things[model_name])

            delattr(handler, '__thing__')


class Menu(object):

    def __init__(self,  url_spec, handler=None, settings=None, name=None, render=None):
        self.url_spec = url_spec
        self.handler = handler
        self.settings = settings
        self.name = name
        self.render = render


class TempateMananger(object):

    def __init__(self):
        self.template_paths = []
        self.ui_paths = []
        self.uis = []

    def is_valid(self):
        """Check the template is empty"""
        return bool(self.template_paths)

    def create_template_loader(self, mgr):
        """Initialize tempate and bind uis:
        param mgr: InventoryManger
        """

        ui_container = UIContainer(self.ui_paths)

        # load ui and bind mapper or thing
        for name, uicls in self.uis:
            mgr.load_mapper(uicls)
            mgr.load_thing(uicls)
            ui_container.put_ui(name, uicls)
        return anthem.ChocoTemplateLoader(self.template_paths, ui_container=ui_container)

    def add_ui_path(self, ui_path):
        """Added Ui tempate path to head"""
        self.ui_paths.insert(0, ui_path)

    def put_ui(self, ui_name, uicls):
        self.uis.append((ui_name, uicls))

    def add_template_path(self, template_path):
        """Added  tempate path to head"""
        self.template_paths.insert(0, template_path)
