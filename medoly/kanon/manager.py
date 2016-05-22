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

import os.path
import logging
from medoly import anthem
from medoly.config import SelectConfig

from tornado.web import RequestHandler

from ._kanon import Melos

from .ctx import AppContext
from choco.ui import UIContainer, UIModule


LOGGER = logging.getLogger("kanon.manager")


class InventoryManager(object):
    """Manage and load app context, mappers and things.

     :param handlercls: the default request handler class for build url route handler.
        Defaults is ``anthem.Handler``
    """

    @staticmethod
    def instance():
        """Get or create an InventoryManager singleton

        :returns: the current InventoryManager singletion
        :rtype: InventoryManager
        """
        if not hasattr(InventoryManager, "_current"):
            InventoryManager._current = InventoryManager()

        return InventoryManager._current

    @staticmethod
    def set_instance(mgr):
        """Set current singleton inventoy manager

        :param InventoryManager mgr: inventoy manager
        :param SelectConfig config: the select config , default create a new empty config
        :param template_mananger: the template mananger for custum template engine
        """
        if isinstance(mgr, InventoryManager):
            InventoryManager._current = mgr
        else:
            raise TypeError("The mgr must be an instance of InventoryManager")

    def __init__(self, handlercls=None, config=None, template_mananger=None):
        #: the boot class instances for bootstrap configuration
        self.boots = []

        #: the applcation context
        self.app_ctx = AppContext()

        #: the config
        self.config = config or SelectConfig()

        #: the model class container
        self.models = {}

        #: the data-mapping layer singletion  instance container
        self.mappers = {}

        #: the thing singleton instance container
        self.things = {}

        #: the url route container list
        self.menus = []

        #: the application name
        self.app_name = "Medoly"

        if handlercls and not issubclass(handlercls, RequestHandler):
            raise TypeError("Must be a subclass of RequestHandler: {0}".format(handlercls.__name__))
        self.defalut_handler = handlercls or anthem.Handler

        #: the choco template manager
        self.template_mananger = template_mananger or TempateMananger()

        #: the custom chords
        self.chords = {}

    def set_app_name(self, name):
        """Set application name"""
        self.app_name = name

    def attach(self, point, callback, failsafe, priority, kwargs):
        """Append a hook"""
        self.app_ctx.attach(point, callback, failsafe, priority, kwargs)

    def error_page(self, status_code, callback):
        """Http exception handler hook

            :param int status_code: http status code
            :param function callback: the excption handle callback
        """
        self.app_ctx.error_page(status_code, callback)

    def load(self):
        self.load_boot()
        self.mount_model()
        self.mount_mapper()
        self.mount_thing()
        self.mount_chord()
        self.mount_menu()
        return self.create_app()

    def load_boot(self):
        from medoly import cmd
        # intialize console option parser
        LOGGER.debug("Parsing console options")
        console = cmd.Cmd('/etc/%s/app.conf' % (self.app_name))
        self.boots = [boot() for boot in self.boots]
        console.parse_cmd(self.app_name, self.boots, self.config)
        self.boot_config()

    def boot_config(self):
        LOGGER.debug("Bootstrap config")
        for boot in self.boots:
            if hasattr(boot, 'setup'):
                boot.setup(self.config, self.app_ctx.settings)

    def create_app(self):
        """Returns an anthem application thats intialize with settings"""
        LOGGER.debug("Creating app!")
        settings = self.intitilaize_app_settings()
        self.app_ctx.settings.update(settings)
        return anthem.Application(self.app_ctx.routes, self.initilaize_app, **self.app_ctx.settings)

    def initilaize_app(self, app):
        """Initilalze and setting application

        #. load hook points
        #. load error page hooks


        :param Applaction app: the modely application
        """
        LOGGER.debug("Starting init app!")
        LOGGER.debug("Start init app hooks!")
        # intialize app hooks
        for (point, callback, failsafe, priority, kwargs) in self.app_ctx.hooks:
            app.attach(point, callback, failsafe, priority, **kwargs)

        # intialize error page hooks
        for (code, func) in self.app_ctx.error_pages.items():
            app.error_page(code, func)

        app.config = self.config

    def intitilaize_app_settings(self):
        settings = dict()
        # try bind template loader
        if self.template_mananger.is_valid():
            LOGGER.debug("Init template!")
            settings['template_loader'] = self.template_mananger.create_template_loader(self)

        # try to setting static resource
        static_path = self.config.get("asset.path")
        if static_path:
            settings['static_path'] = static_path
        static_url_prefix = self.config.get("asset.url_prefix")
        if static_url_prefix:
            settings['static_url_prefix'] = static_url_prefix

        settings['debug'] = self.config.get("debug", False)
        settings['cookie_secret'] = self.config.get("secert_key", None)

        return settings

    def put_chord(self, chord_name, chord_class, **settings):
        """Added a chord"""
        LOGGER.debug("Putting chord:{%s -> %r}", chord_name, chord_class)
        if chord_name in self.chords:
            raise InventoryExistError("chord for ```{}`` exists.".format(chord_name))
        self.chords[chord_name] = (chord_class, settings)

    def put_ui(self, ui_name, uicls):
        """Added a ui"""
        LOGGER.debug("Putting ui:{%s -> %r}", ui_name, uicls)
        if ui_name in self.template_mananger.uis:
            raise InventoryExistError("UI for ```{}`` exists.".format(ui_name))
        if not issubclass(uicls, UIModule):
            classes = [UIModule] + self.get_class_bases(uicls)
            uicls = type(uicls.__name__, tuple(classes), dict(uicls.__dict__))

        self.template_mananger.put_ui(ui_name, uicls)

    def put_boot(self, boot):
        """Add a boot config"""
        LOGGER.debug("Puting boot:%s", boot.__name__)
        self.boots.append(boot)

    def put_model(self, name, model):
        """Add a model"""
        LOGGER.debug("Puting model:{%s -> %r}", name, model)
        if name in self.models:
            raise InventoryExistError("Model for ```{}`` exists.".format(name))

        self.models[name] = model

    def put_mapper(self, name, mapper):
        """Add a mapper"""
        LOGGER.debug("Puting mapper:{%s -> %r}", name, mapper)
        if name in self.mappers:
            raise InventoryExistError("Backend for ```{}`` exists.".format(name))

        self.mappers[name] = mapper

    def put_thing(self, name, thing):
        """Add a thing"""
        LOGGER.debug("Puting thing:{%s -> %r}", name, thing)
        if name in self.things:
            raise InventoryExistError("Thing for ```{}`` exists.".format(name))

        self.things[name] = thing

    def add_template_path(self, template_path):
        """Added a template path in template manager"""
        LOGGER.debug("Adding template path: '%s'", template_path)
        self.template_mananger.add_template_path(template_path)
        ui_path = os.path.join(template_path, "ui")
        if os.path.isdir(ui_path):
            LOGGER.debug("Adding template ui path : '%s'", ui_path)
            self.template_mananger.add_ui_path(ui_path)

    def add_route(self, url_spec, handler=None, settings=None, name=None, render=None):
        """Add a url route"""
        self.menus.append(Menu(url_spec, handler, settings, name, render))

    def mount_chord(self):
        """Registe the melos for  the  chord class"""

        for chord_name in self.chords:
            chord, settings = self.chords.get(chord_name)
            self.load_meloes(chord)
            bean = settings.get('bean')
            if bean:
                self.chords[chord_name] = chord()
            else:
                self.chords[chord_name] = chord

        setattr(anthem.handler, "__chord", self.chords)

    def mount_model(self):
        """Sets Model"""
        setattr(anthem.handler, '__model', self.models)

    def mount_mapper(self):
        """Initailize and regiest the backend"""
        mappers = {}
        for mapper_name in self.mappers:
            mapper = self.mappers.get(mapper_name)
            mappers[mapper_name] = mapper()

        self.mappers = mappers
        setattr(anthem.handler, '__backend', mappers)

    def mount_thing(self):
        """Initailize and regiest the thing"""
        things = {}
        for thing_name in self.things:
            thing = self.things.get(thing_name)
            things[thing_name] = thing()

        self.things = things
        setattr(anthem.handler, '__thing', things)

    def mount_menu(self):
        """Intialize the url routes and handlers"""
        for menu in self.menus:
            self.connect(menu.url_spec, menu.handler,
                         menu.settings, menu.name, menu.render)

    def connect(self, url_spec, handler=None, settings=None, name=None, render=None):
        """Add a route 

         if render is ``true``,  it is a simple template request handler.

        :param url_spec: the url path
        :type url_spec: url
        :param handler:  the handler class, defaults using the manager ``default_hander``
        :param settings: the default intailize setting for handler, Optional.
        :param render: the render template path
        :type render: string, optional
        :raises: ValueError
        """

        #: if render is ``true``,  it is a simple template request handler
        if render:
            self.app_ctx.routes.append((url_spec, anthem.RenderHandler, dict(template=render)))
            return

        if handler is None:
            raise ValueError("Handler is required, can't be empty")

        # DI: mapper and thing
        self.load_meloes(handler)

        #: check inhert handler class, if not, inject the default handler class
        if not issubclass(handler, RequestHandler):
            classes = [self.defalut_handler] + self.get_class_bases(handler)
            handler = type(handler.__name__, tuple(
                classes), dict(handler.__dict__))

        self.app_ctx.routes.append(anthem.url(url_spec, handler, settings, name))

    def get_class_bases(self, klass):
        """Getting the base classes excluding the type<object>"""
        bases = klass.__bases__
        if len(bases) == 1 and bases[0] == object:
            return []
        else:
            return list(bases)

    def load_meloes(self, kclass):
        """Load inventory for the kclasss

        Examples:

        .. code: python

            class Index(object):
                user_thing  = Melos("thing:User")
                # default  is a thing inventory
                post_thing = Melos("Post")

        The  dependecy injection, it will load the relational inventory instacne by the  melos of class had and assign to the named class variable.

        """

        attrs = kclass.__dict__
        for k, v in attrs.iteritems():
            if isinstance(v, Melos):
                inventory = self._load_melos(v)
                if not inventory:
                    raise ValueError("Can't found inventory for ``%s``." % (v.inventory_name))
                setattr(kclass, k, inventory)

    def _load_melos(self, melos):
        """ Get the inventory by melos"""
        if melos.genre == "thing":
            return self.things.get(melos.name)
        elif melos.genre == "mapper":
            return self.mappers.get(melos.name)
        elif melos.genre == "model":
            return self.models.get(melos.name)
        elif melos.genre == "chord":
            return self.chords.get(melos.name)


class InventoryExistError(Exception):
    """Invenort exist exception"""
    pass


class Menu(object):
    """Url Menu

        if  ``render`` is not ``None``, it will use the template render. else set the ``handler``.

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

    def __init__(self, url_spec, handler=None, settings=None, name=None, render=None):

        self.url_spec = url_spec
        self.handler = handler
        self.settings = settings
        self.name = name
        self.render = render


class TempateMananger(object):
    """Template Mannager
    """

    def __init__(self):
        self.template_paths = []
        self.ui_paths = []
        self.uis = {}

    def is_valid(self):
        """Check the template is empty"""
        return bool(self.template_paths)

    def create_template_loader(self, mgr):
        """Initialize tempate and bind uis

        :param mgr: InventoryManger
        """

        ui_container = UIContainer(self.ui_paths)

        # load ui and bind mapper or thing
        for name, uicls in self.uis.items():
            mgr.load_meloes(uicls)
            ui_container.put_ui(name, uicls)
        return anthem.ChocoTemplateLoader(self.template_paths, ui_container=ui_container,
                                          filesystem_checks=mgr.config.get(
                                              "choco.filesystem_checks", False),
                                          module_directory=mgr.config.get("choco.cache_path"))

    def add_ui_path(self, ui_path):
        """Add Ui tempate path to head"""
        self.ui_paths.insert(0, ui_path)

    def put_ui(self, ui_name, uicls):
        """Put ui in  uis

        :param string ui_name: ui template name
        :param uicls: UI Module class instance
        """
        self.uis[ui_name] = uicls

    def add_template_path(self, template_path):
        """Add  tempate path to head"""
        self.template_paths.insert(0, template_path)
