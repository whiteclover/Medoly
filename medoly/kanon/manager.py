import os.path
import re
import logging
from medoly import anthem


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
        """
        if isinstance(mgr, InventoryManager):
            InventoryManager._current = mgr
        else:
            raise TypeError("The mgr must be an instance of InventoryManager")

    def __init__(self, handlercls=None):
        #: the boot class instances for bootstrap configuration
        self.boots = []

        #: the applcation context
        self.app_ctx = AppContext()

        #: the config
        self.config = None

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

        self.defalut_handler = handlercls or anthem.Handler

        #: the choco template manager
        self.template_mananger = TempateMananger()

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
        self.mount_menu()
        return self.create_app()

    def load_boot(self):
        from medoly import cmd
        # intialize console option parser
        LOGGER.debug("Parsing console options")
        console = cmd.Cmd('/etc/%s/app.conf' % (self.app_name))
        self.boots = [boot() for boot in self.boots]
        self.config = console.parse_cmd(self.app_name, self.boots)
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

    def put_ui(self, ui_name, uicls):
        if not issubclass(uicls, UIModule):
            classes = [UIModule] + self.get_class_bases(uicls)
            uicls = type(uicls.__name__, tuple(classes), dict(uicls.__dict__))

        LOGGER.debug("Putting ui:{%s -> %r}", ui_name, uicls)
        self.template_mananger.put_ui(ui_name, uicls)

    def put_boot(self, boot):
        LOGGER.debug("Puting boot:%s", boot.__name__)
        self.boots.append(boot)

    def put_model(self, name, model):
        LOGGER.debug("Puting model:{%s -> %r}", name, model)
        self.models[name] = model

    def put_mapper(self, name, mapper):
        LOGGER.debug("Puting mapper:{%s -> %r}", name, mapper)
        self.mappers[name] = mapper

    def put_thing(self, name, thing):
        LOGGER.debug("Puting thing:{%s -> %r}", name, thing)
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

        #: if render is ``true``,  it is a simple template request handler
        if render:
            self.app_ctx.routes.append((url_spec, anthem.RenderHandler, dict(template=render)))
            return

        if handler is None:
            raise ValueError("Handler is required, can't be empty")

        # DI: mapper and thing
        self.load_mapper(handler)
        self.load_thing(handler)

        #: check inhert handler class, if not, inject the default handler class
        if not issubclass(handler, self.defalut_handler):
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

    def load_mapper(self, handler):
        """Mapper Dependency injection, check the line split here doc "__mapper__"

        rule::

            $variableName->$mapperName

        Example:

        .. code:: python

            class Index(object):

                __mapper__ = '''userMapper->User
                postMapper->Post'''

                def get(self):
                    pass

        The mapper dependecy injection, it will load the mapper instacne by the backend name and assign to the named class variable.



        .. code:: python

            class Index(object):

                userMapper = Backend("User")
                postMapper = Backend("Post")


                def get(self):
                    pass

        """
        REG = re.compile(r"(\w[\w\d_]+)\s*\-\s*>\s*(\w[\w\d_]+)")
        doc = getattr(handler, '__mapper__', "")
        if doc:
            lines = [part.strip() for part in doc.split("\n") if part.strip()]
            for line in lines:
                match = REG.match(line)
                if match:
                    name, model_name = match.group(1), match.group(2)
                    setattr(handler, name, self.mappers[model_name])

            delattr(handler, '__mapper__')

    def load_thing(self, handler):
        """Thing Dependency injection, check the line split here doc "__thing__"

        Line Rule::

            $variableName->$thingName

        Example:

        .. code:: python

            class Index(object):

                __thing__ = '''userThing->User
                postThing->Post'''

                def get(self):
                    pass

        The thing dependecy injection, it will load the thing instacne by the thing name and assign to the named class variable.



        .. code:: python

            class Index(object):

                userThing = Thing("User")
                postThing = Thing("Post")


                def get(self):
                    pass

        """
        REG = re.compile(r"(\w[\w\d_]+)\s*\-\s*>\s*(\w[\w\d_]+)")
        doc = getattr(handler, '__thing__', "")
        if doc:
            lines = [part.strip() for part in doc.split("\n") if part.strip()]
            for line in lines:
                match = REG.match(line)
                if match:
                    name, model_name = match.group(1), match.group(2)
                    setattr(handler, name, self.things[model_name])

            delattr(handler, '__thing__')


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
        self.uis = []

    def is_valid(self):
        """Check the template is empty"""
        return bool(self.template_paths)

    def create_template_loader(self, mgr):
        """Initialize tempate and bind uis

        :param mgr: InventoryManger
        """

        ui_container = UIContainer(self.ui_paths)

        # load ui and bind mapper or thing
        for name, uicls in self.uis:
            mgr.load_mapper(uicls)
            mgr.load_thing(uicls)
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
        self.uis.append((ui_name, uicls))

    def add_template_path(self, template_path):
        """Add  tempate path to head"""
        self.template_paths.insert(0, template_path)
