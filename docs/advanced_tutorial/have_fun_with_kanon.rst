Have Fun with kanon
++++++++++++++++++++++++++++

Kanon is a inventory composer, it combines model, thing, mappper, handler, route, boot and so on all thing togther. 
Inventory is a resource like mapper inventory, model inventory, chord inventory and thing inventory.


bloom
================

kanon ``bloom`` decorator is used to register Thing, Model, and Mapper.


model
----------------

When sets the bloom type to "model", it will register current class as Model inventory. Defaultly, ``bloom`` register the model using the model class name.

.. code-block:: python

    @bloom("model")
    class User(object):

        def __init__(self, uid, name):
            self.uid = uid
            self.name = name

        def __json__(self):
            return {"uid": self.uid, "name": self.name}


mapper
----------------

When sets the bloom type to "mapper", it will register current class as Backend inventory.

If the mapper class ends with the postfix "Mapper", if will use  striped the end postfix register named ``User``. otherwise register with the
mapper class name defaultly.

.. code-block:: python

    @bloom("mapper")
    class UserMapper(object):

        def find_by_uid(self, uid):
            return User(uid, "Anna")


thing
----------------

When sets the bloom type to "thing", it will register current class as Thing inventory.

If the thing class ends with the postfix "Thing", if will use  striped the end postfix register named ``User``. otherwise register with
the thing class name defaultly.

.. code-block:: python

    @bloom("thing")
    class UserThing(object):

        def __init__(self):
            self.mapper = Backend('User')

        def find_by_uid(self, uid):
            return self.mapper.find_by_uid(uid)



Customize the kanon inventory access name
----------------------------------------------------------------------

if you wanna use custom name, adding the ``access_name`` in the ``bloom`` decorator:


.. code-block:: python

    @bloom("model", access_name="custom_name")
    #@bloom("model", "custom_name") # the same as blow
    class CustomNameModel(object):

        def __init__(self, uid, name):
            self.uid = uid
            self.name = name

        def __json__(self):
            return {"uid": self.uid, "name": self.name}


.. important::
    For every same inventory type, the inventory access name is unique. if ``bloom`` register a  inventory using repeat access name, 
    kanon will raise inventory exist error.


menu
=================


kanon ``menu`` decorator is used to link request handler with url path route.


.. code-block:: python

    @menu("/user")
    class UserPage(anthem.Handler):

        def get(self):
            uid = int(self.get_argument("uid"))
            self.render("user_index.html", uid=uid)


Linking  a named request handler
------------------------------------------------------

Defaultly, ``menu`` does not set the name for the handler, if you wanna use the ``reverse_url`` method to  build a url path throught the name, just added
the ``name`` argument in ``menu`` decorator:

.. code-block:: python

    @menu("/post", name="post_new_page")
    class PostCreatePage(anthem.Handler):

        def get(self):
            self.render("post_create.html")


chord
==================

kanon ``chord`` decorator is used to register a Chord inventory.


.. code-block:: python

    @chord()
    class AuthManager(object):
        pass


Defaultly, ``chord``  set the chord class name as access name, you can also set the customize name:



.. code-block:: python

    @chord("custom_name") # same as @chord(name="custom_name")
    class CustomizeNameManager(object):
        pass



If set ``bean``  to ``True`` in ``chord`` decorator, it will register the chord class and initialize a instance in it. otherwise when use ``muses.Chord``
to get the chord resource, you just get a chord class. more information see the `muses`.

ui
================

kanon ``menu`` decorator is used to add a ui module. more information see the `Template and UI <../advanced_tutorial/template_and_ui.html>`_
section.

.. code-block:: python
    
    @kanon.ui("hotpost.html")
    class HotPost(object):

        hot_post_thing = Melos("HotPost")

        def render(self, item_size=10):
            posts = self.hot_post_thing(item_size)
            return {"posts": posts}



boot
=====================


kanon ``boot`` decorator is used to configuration the application bootstrap process, integrating command-line options and setup third-patry resources.


.. code-block:: python

    @kanon.boot()
    class WebBoot(object):

        def config(self, options):
            """Web settings"""
            group = options.group("Web settings")
            _ = group.define
            _('--web.cookie_secret', default="secert_key", 
              help='The secert key for secure cookies (default %(default)r)')

        def setup(self, config, settings):
            """Ensure web settings"""
            config.set("web.xsrf_cookies", True)
            config.set("web.login_url", "/auth/login")


In the above code, the ``boot`` and a WebBoot configuration class. it will add a  group command line option use the ``config`` method.
it uses the ``setup`` method to sets the tornado application confirmed ``xsrf_cookies`` and ``login_url`` settings, and a configurable
``cookie_secret`` setting. More information see the `config<config>`_  section.

Add error page handler
========================

kanon ``error_page`` decorator is used to add a http status error handler process. it can process all http status expection error.

For example, add a 404 page handler:

.. code-block:: python

  @kanon.error_page(404)
  def not_found(req_handler, code, **kw):
      """Not Found Page"""
      req_handler.render("404.html", page_title='Page Not Found')

 
Adding a 500 status code page handler:

.. code-block:: python

  @kanon.error_page(500)
  def internal_error(req_handler, code, **kw):
      """Internal Error Page"""
      req_handler.render("500.html", page_title='Internal Error')



Add hook pointer
====================


kanon ``hook`` decorator is used to add request hook pointer.

Cuttently, hook supports fourth hook entry pointer:

:on_start_request: Running on the request handler ``perpare`` mehtod
:on_end_request: Running on the request handler ``on_finish`` mehtod
:before_error_response: Runnig on the error expection request, implements hook on  the ``write_error`` begining .
:after_error_response: Runnig on the error expection request,  implements  hook on the ``write_error`` ending.


Add two process handlers on ``on_start_request`` hook pointer:

.. code-block:: python

  @kanon.hook("on_start_request")
  def on_load(req_handler):
      print("on load req_handler: %s", req_handler)

  @kanon.hook("on_start_request")
  def on_start_request(req_handler):
      """on start request hook"""
      session.load(req_handler)

Defaultly, ``hook`` decorator with ``priority`` value is 50, the application will run hooks on the register order.
You can set a higher ``priority`` value  to prioritize the hook method.  Priority numbers should be limited to the closed interval [0, 100].


.. code-block:: python

  @kanon.hook("on_start_request")
  def on_load(req_handler):
      print("This will after on_session, on load req_handler: %s", req_handler)

  @kanon.hook("on_start_request", priority=60)
  def on_session(req_handler):
      """on start request hook"""
      session.load(req_handler)


Bootstrap the application
============================


Overview
-------------------------

The ``compose`` method is the kanon magic method. it scans a python module package, then every kanon decorator in the above will be called.
Also it check the module package whether or not a  folder package to configuration template engine paths.

The ``chant`` method is  used to bootstrap every thing and create the application instance. Firstly parses the command-line and bootstrap the boot config. 
Then loads the inventory in the ``muses`` and bootstraps application setting and creates the anthem application.

For example,  int the demo project (the source in the ``examples/demo`` directory) has a app module.



.. code-block:: text

  ├─app
  │  │  boot.py # boot settings
  │  │  filters.py # http hook filter
  │  │  index.py # home menu
  │  │  __init__.py
  │  │
  │  ├─ asset # default static asset path
  │  ├─template # template path
  │  │  │  404.html
  │  │  │  index.html
  │  │  │  user_index.html
  │  │  │
  │  │  └─ui # ui module template path
  │  │          user.html
  │  │
  │  └─user # user module
  │          mapper.py
  │          model.py
  │          thing.py
  │          ui.py
  │          view.py
  │          __init__.py


Calls the ``compose`` method and chant then a tornado application has builded:

.. code-block:: python

     kanon.compose("app")
     app = kanon.chant()

Configure the url prefix
-----------------------------------------------

In the above example, the  ``compose``  uses the  ``menu``  to link  every url path in the root path. you can set a url_prefix to let the  ``compose``
link every menu path in a sub path:


In the beblow example, it links every url path in ``app`` module menu to the sub path ``/app``,  ``admin`` module menu to the sub path ``/admin``

.. code-block:: python

     kanon.compose("app", url_prefix="/app")
     kanon.compose("admin", url_prefix="/admin")
     app = kanon.chant()


Configure the template path
-----------------------------------------------

In the above example, the  ``compose``  check the app module, and find a template folder named `template` in the root module path, then append the 
template path in the head  template paths of  the template manager. 


In the beblow example, in app module  checks the root path `template` , and in admin module  checks the `admin_template` path.

.. code-block:: python

     kanon.compose("app")
     kanon.compose("admin", template_path="admin_template")
     app = kanon.chant() # bootstrap and create the tornado application