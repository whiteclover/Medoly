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

"""Kanon managers"""

import os.path
import logging
import re
import types

from tornado.web import RequestHandler

from medoly import anthem
from medoly import muses
from medoly.config import SelectConfig
from medoly import cmd
from medoly.template.engine import TemplateEngine
from medoly.util import get_class_bases
from ._kanon import Melos
from .ctx import AppContext


LOGGER = logging.getLogger("kanon.manager")


class InventoryManager(object):
    """Manage and load app context, mappers and things.

    :param handlercls: the default request handler class for build url route handler.
        Defaults is ``anthem.Handler``.
    :param SelectConfig config: the select config , default create a new empty config
    :param template_manager: the template mananger for custum template engine
    :param bool enable_cmd_parse: when set to False to disable the console command pasre.
            Defaults to   ``True`` enable the terminal command option.
    :param url_pattern_manager: the url pattern process manager.
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
        """
        if isinstance(mgr, InventoryManager):
            InventoryManager._current = mgr
        else:
            raise TypeError("The mgr must be an instance of InventoryManager")

    def __init__(self, handlercls=None, config=None, template_manager=None, enable_cmd_parse=True,
                 url_pattern_manager=None):

        #: the current compose context url prefix
        self.compose_url_prefix = ""
        #: the terminal parse controll
        self.enable_cmd_parse = enable_cmd_parse

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
        self.template_manager = template_manager or TempateMananger()

        #: the url pattern processor
        self.url_pattern_manager = url_pattern_manager or URLPatternManager()

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
        """Loads all invenory settings and create the anthem application"""
        self.load_boot()
        self.mount_model()
        self.mount_mapper()
        self.mount_thing()
        self.mount_chord()
        self.mount_menu()
        return self.create_app()

    def load_boot(self):
        """Loads boot config"""
        # intialize console option parser
        if self.enable_cmd_parse:
            LOGGER.debug("Parsing console options")
            console = cmd.Cmd('/etc/%s/app.conf' % (self.app_name))
            self.boots = [boot() for boot in self.boots]
            config = console.parse_cmd(self.app_name, self.boots)
            self.config.update(config)
            LOGGER.info("The application config: %s", self.config)
        self.boot_config()

    def boot_config(self):
        """Bootstrap boot config setup"""
        LOGGER.debug("Bootstrap config")
        for boot in self.boots:
            if hasattr(boot, 'setup'):
                boot.setup(self.config, self.app_ctx.settings)

    def config_from_file(self, path):
        """Loads config from file"""
        config = cmd.config_from_file(path)
        self.config.update(config)

    def create_app(self):
        """Returns an anthem application thats intialize with settings"""
        LOGGER.debug("Creating app!")
        settings = self.initialize_app_settings()
        self.app_ctx.settings.update(settings)
        return anthem.Application(self.app_ctx.routes, self.initilaize_app, **self.app_ctx.settings)

    def initilaize_app(self, app):
        """Initilalze and setting application

        #. load hook points
        #. load error page hooks


        :param Applaction app: the medoly application
        """
        LOGGER.debug("Starting Initialize app!")
        LOGGER.debug("Starting initilaize app hooks!")
        # initialize app hooks
        for (point, callback, failsafe, priority, kwargs) in self.app_ctx.hooks:
            app.attach(point, callback, failsafe, priority, **kwargs)

        # initialize error page hooks
        for (code, func) in self.app_ctx.error_pages.items():
            app.error_page(code, func)

        app.config = self.config

    def initialize_app_settings(self):
        """Initialize the application settings

        #. Load and create template loader
        #. Load web config firstly
        #. Load the  static asset settings
        #. If has global debug setting, override it.
        """
        settings = dict()
        # try bind template loader
        if self.template_manager.is_valid():
            LOGGER.debug("Init template!")
            settings['template_loader'] = self.template_manager.create_template_loader(self)

        #: load web settings firstly
        settings.update(self.config.get("web", {}))

        # try to setting static resource
        static_path = self.config.get("asset.path")
        if static_path:
            settings['static_path'] = static_path
        static_url_prefix = self.config.get("asset.url_prefix")
        if static_url_prefix:
            settings['static_url_prefix'] = static_url_prefix

        #: If has global debug setting, override it.
        debug = self.config.get("debug")
        if debug is not None:
            settings['debug'] = debug
        settings['cookie_secret'] = self.config.get("secert_key", None)

        return settings

    def put_chord(self, chord_name, chord_class, **settings):
        """Adds a chord"""
        LOGGER.debug("Putting chord:{%s -> %r}", chord_name, chord_class)
        if chord_name in self.chords:
            raise InventoryExistError("chord for ```{}`` exists.".format(chord_name))
        self.chords[chord_name] = (chord_class, settings)

    def put_ui(self, ui_name, uicls):
        """Adds a ui"""
        LOGGER.debug("Putting ui:{%s -> %r}", ui_name, uicls)
        if ui_name in self.template_manager.uis:
            raise InventoryExistError("UI for ```{}`` exists.".format(ui_name))

        self.template_manager.put_ui(ui_name, uicls)

    def put_boot(self, boot):
        """Adds a boot config

        If the boot is a function, then call the function gets a chain config boots, then add them in manager boot list,
        else appends it to manager boot  list.
        """
        LOGGER.debug("Puting boot:%s", boot.__name__)
        if isinstance(boot, types.FunctionType):
            boots = boot()
            for boot_config in boots:
                self.boots.append(boot_config)
        else:
            self.boots.append(boot)

    def put_model(self, name, model):
        """Adds a model"""
        LOGGER.debug("Puting model:{%s -> %r}", name, model)
        if name in self.models:
            raise InventoryExistError("Model for ```{}`` exists.".format(name))

        self.models[name] = model

    def put_mapper(self, name, mapper):
        """Adds a mapper"""
        LOGGER.debug("Puting mapper:{%s -> %r}", name, mapper)
        if name in self.mappers:
            raise InventoryExistError("Backend for ```{}`` exists.".format(name))

        self.mappers[name] = mapper

    def put_thing(self, name, thing):
        """Adds a thing"""
        LOGGER.debug("Puting thing:{%s -> %r}", name, thing)
        if name in self.things:
            raise InventoryExistError("Thing for ```{}`` exists.".format(name))

        self.things[name] = thing

    def add_template_path(self, template_path):
        """Adds a template path in template manager"""
        LOGGER.debug("Adding template path: '%s'", template_path)
        self.template_manager.add_template_path(template_path)

    def add_route(self, url_spec, handler=None, settings=None, name=None, render=None):
        """Adds a url route

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

        self.menus.append(Menu(self.compose_url_prefix + url_spec, handler, settings, name, render))

    def mount_chord(self):
        """Register the melos for  the  chord class"""

        for chord_name in self.chords:
            chord, settings = self.chords.get(chord_name)
            self.load_melos(chord)
            bean = settings.get('bean')
            if bean:
                self.chords[chord_name] = chord()
            else:
                self.chords[chord_name] = chord

        setattr(muses, "__chord", self.chords)

    def mount_model(self):
        """Sets Model"""
        setattr(muses, '__model', self.models)

    def mount_mapper(self):
        """Initialize and regiest the backend"""
        mappers = {}
        for mapper_name in self.mappers:
            mapper = self.mappers.get(mapper_name)
            mappers[mapper_name] = mapper()

        self.mappers = mappers
        setattr(muses, '__backend', mappers)

    def mount_thing(self):
        """Initialize and regiest the thing"""
        things = {}
        for thing_name in self.things:
            thing = self.things.get(thing_name)
            things[thing_name] = thing()

        self.things = things
        setattr(muses, '__thing', things)

    def mount_menu(self):
        """Initialize the url routes and handlers"""
        for menu in self.menus:
            self.connect(menu.url_spec, menu.handler,
                         menu.settings, menu.name, menu.render)

    def connect(self, url_spec, handler=None, settings=None, name=None, render=None):
        """Adds a route

        If  ``render`` is not ``None``, it will use the template render hanlder, else use the ``handler`` as request handler class.

        :param url_spec: the url path
        :type url_spec: url
        :param handler:  the handler class, defaults using the manager ``default_hander``
        :param settings: the default intailize setting for handler, Optional.
        :param render: the render template path
        :type render: string, optional
        :raises: ValueError
        """
        # Preprocess url rule
        url_spec = self.url_pattern_manager.url(url_spec)
        #: if render is ``true``,  it is a simple template request handler
        if render:
            self.app_ctx.routes.append(anthem.url(url_spec, anthem.RenderHandler, dict(template=render), name))
            return

        if handler is None:
            raise ValueError("Handler is required, can't be empty")

        # DI: mapper and thing
        self.load_melos(handler)

        #: check inhert handler class, if not, inject the default handler class
        if not issubclass(handler, RequestHandler):
            classes = [self.defalut_handler] + get_class_bases(handler)
            handler = type(handler.__name__, tuple(
                classes), dict(handler.__dict__))

        self.app_ctx.routes.append(anthem.url(url_spec, handler, settings, name))

    def load_melos(self, kclass):
        """Loads the inventory for the kclasss

        Examples:

        .. code-block:: python

            class Index(object):
                user_thing  = Melos("thing:User")
                # default  is a thing inventory
                post_thing = Melos("Post")

        The  dependecy injection, it will load the relational inventory instacne by the  melos of class ,
        and assign to the named class variable.

        """

        attrs = kclass.__dict__
        for k, v in attrs.iteritems():
            if isinstance(v, Melos):
                inventory = self._load_melos(v)
                if not inventory:
                    raise ValueError("Can't found inventory for ``%s``." % (v.inventory_name))
                setattr(kclass, k, inventory)

    def _load_melos(self, melos):
        """ Gets the inventory by melos"""
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


class URLPatternManager(object):
    """The Url pattern processor

    Examples::

        @kanona.menu("/post/{post_id:int}")
        class PostView(anthem.Handler):

            def get(self, post_id):
                post_id = int(post_id)
                self.jsonify({"post_id": post_id})


    """

    RULE_RE = re.compile(
        r"""\{([a-zA-Z_][a-zA-Z0-9_]*)(?::([a-zA-Z_][a-zA-Z0-9_]*|\(.*\)))?\}""")
    """The defaults url regex expresion rule"""

    DEFAULT_PATTERNS = {
        'int': r'-?\d+',
        'any': r'[^/]+',
        'float': r'-?\d+\.\d+',
    }
    """The defaults url patterns"""

    def __init__(self):
        self.patterns = self.DEFAULT_PATTERNS.copy()

    def add_pattern(self, name, pattern):
        """Adds a url pattern rule

        Example:

        .. code-block:: python

            >>> pattern_mgr  = URLPatternManager()
            >>> pattern_mgr.add_pattern("yymm", r"\d\d\d\d")
            >>> pattern_mgr.url("/{date:yyymm}")
            >>> ... "/(?P<date>\d\d\d\d)"


        :param name: the rule pattern name
        :type name: string
        :param pattern: the regex expression is used to converted.
        :type pattern: string
        """
        self.patterns[name] = pattern

    def url(self, rule):
        """Converts to url regex express rule"""
        end = 0
        ms = self.RULE_RE.finditer(rule)
        pattern = ''
        regex = False
        if ms:
            for m in ms:
                regex = True
                label, rule_name = m.group(1), m.group(2) or 'any'
                regex = self.patterns.get(rule_name)
                pattern += rule[end:m.start()]
                if regex:
                    pattern += '(?P<%s>%s)' % (label, regex)
                else:
                    pattern += '(?P<%s>%s)' % (label, rule_name[1:-1])
                end = m.end()

        if regex:
            pattern += rule[end:]
            pattern = '%s' % pattern
        else:
            pattern = rule

        return pattern


class TempateMananger(object):
    """Template Mannager

    Currently, supports choco, mako, jinja2, selene (tornado default tempate).

    :param template_engine: The default tempalte egine, Defaults None, you need
        load the template engine using ``load_template_engine``.
    :param string ui_path: the default ui path for template loading, Defaults to "ui".
    """

    def __init__(self, template_engine=None, ui_path="ui"):
        self.template_paths = []
        self.ui_path = ui_path
        self.ui_paths = []
        self.uis = {}

        #: the template engine
        self.__template_engine = template_engine

    def load_template_engine(self, engine_name):
        """Load and create template engine info
        If the template engine had loaded, it will skip reload a new engine.

        Currently, supports choco, mako, jinja2, selene (tornado default tempate).

        :param engine_name:  the template engine name
        :type engine_name: [type]
        """
        if self.__template_engine:
            LOGGER.warning("The template engine ``%s`` has loaded", engine_name)
        else:
            LOGGER.info("Creating template engine ``%s``.", engine_name)
            self.__template_engine = TemplateEngine(engine_name)

    def is_valid(self):
        """Checks the template is empty"""
        return bool(self.template_paths)

    def create_template_loader(self, mgr):
        """Initialize tempate and bind uis

        :param mgr: InventoryManger
        """
        namespace = {}
        template_engine = mgr.config.get("template_engine", "jinja2")
        self.load_template_engine(template_engine)
        template_settings = mgr.config.get("template_setting", {})
        namespace.update(template_settings)
        ui_container = None
        if self.ui_support:
            ui_container = self.load_ui_container(mgr)

        return self.__template_engine.create_template_loader(self.template_paths, ui_container, namespace)

    @property
    def ui_support(self):
        """Check the template engine is support ui module featue"""
        if self.__template_engine is not None:
            return self.__template_engine.ui_support

    def load_ui_container(self, mgr):
        """Loads ui container"""
        LOGGER.debug("Loading ui modules.")
        ui_container = self.__template_engine.ui_container_cls(self.ui_paths)

        #: Load ui and bind mapper or thing
        ui_module_cls = self.__template_engine.ui_module_cls
        for name, uicls in self.uis.items():
            if not issubclass(uicls, ui_module_cls):
                classes = [ui_module_cls] + get_class_bases(uicls)
                uicls = type(uicls.__name__, tuple(classes), dict(uicls.__dict__))
            mgr.load_melos(uicls)
            ui_container.put_ui(name, uicls)
        return ui_container

    def add_ui_path(self, ui_path):
        """Adds Ui tempate path to head"""
        self.ui_paths.insert(0, ui_path)

    def put_ui(self, ui_name, uicls):
        """Puts ui in  uis

        :param string ui_name: ui template name
        :param uicls: UI Module class instance
        """
        self.uis[ui_name] = uicls

    def add_template_path(self, template_path):
        """Adds tempate path to head"""
        self.template_paths.insert(0, template_path)
        ui_path = os.path.join(template_path, self.ui_path)
        if os.path.isdir(ui_path):
            LOGGER.debug("Adding template ui path : '%s'", ui_path)
            self.add_ui_path(ui_path)
