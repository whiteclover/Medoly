Template and UI
+++++++++++++++++++

Currently, Medoly supports jinja2 , mako Template engines, and two special Template engines with ui features:   selene (Tornado Fork Template Engine) , choco (mako Fork Template Engine).

UI
===============

Ui is a trickly feature, it mostly like Tornado original UIModule,  reusable UI widgets and logic handler. However they is not support to package with their own CSS and JavaScript like Tornado original UIModule. Yep, The Medoly ui modules haven't this feature.


.. note::
    Currently, onyl choco and selene template engines support the ui feature.

For examplse, in a blog system  has a hot post widget to display the hotest posts in home page. you can use the ui to implement it.

Firstly, writing a ``HotPostView`` ui class:


.. code-block:: python
    
    @kanon.ui("hotpost.html")
    class HotPost(object):

        hot_post_thing = Melos("HotPost")

        def render(self, item_size=10):
            posts = self.hot_post_thing(item_size)
            return {"posts": posts}


The kanon ``ui`` decorator  sets the ``HotPost``  render to ``hotpost.html`` template in template ui paths, and register the ui module in template manager.Defaultly  registers the ui class name  to identify the ui moduel, if not set the ``name`` in the kaonan``ui`` decorator.

Then add a normal template in the default ui template  path ``template/ui``.

``hotpost.html``:

.. code-block:: html+mako

    % for post in posts:
    <div>
        <p> ${post.title}</p>
        <div>${post.content}</div>
    </div>
    % end for



Template and UI Layout
========================

Defautly, when medoly ``compose`` scans a package module, it will check whether has a folder named ``template`` in the top level  module folder.
If has, it will push it in the  template paths  for the template engine to render the templates, and at same time if  has a folder in the template path named ``ui``
the medoly will add the ui path in the template manager.

When calls ``kanon.chant`` to boot the application, the template manager will check the current template engine whether supports the ui feature. if does, load the ui container and boot the template loader with ui modules.


For example, in the ``A  Blog Service with SQLAlchemy`` section, the application scans the ``blog.app`` module finding the template path in the top level module, then push it in the head of template paths.  

In the example ``example/demo`` use the ``choco``  template engine, and create a  user widget module:


example/demo/app/user/ui.py

.. code-block:: python


    @kaon.ui("user.html")
    class UserView(object):

        thing = Melos("User")

        def render(self, uid):
            user = self.thing.find_by_uid(uid)
            return {"user": user}


example/demo/app/template/ui/user.html

.. code-block:: html+mako

    <div>
        <p> Name: ${user.name}</p>
        <p> Uid: ${user.uid} </p>
    </div>


Template engine configuration
===============================


Medoly default template engine is ``jinja2``, here are the template engines medoly supports:

    :choco: the choco template engine
    :jinja2: the jinja2 template engine
    :selene: the selene template engine
    :mako: the mako template engine

If medoly find the application setting a namespace key  named   ``template_engine``, then it will try to load the template engine adapter by it.


Setting template configuration
----------------------------------------------

The medoly sets the template loader settings using the configuration in  ``template_setting`` configuration namespace.

An example about choco template configuration in ``example/demo/app/boot.py``:

.. code-block:: python

    @kanon.boot()
    class TemplateBoot(object):
        """Choco template options"""

        def config(self, options):
            group = options.group("Template settings")
            _ = group.define
            _("--template_engine", default="choco", help="Template engine name")
            _('--template_setting.module_directory', default=None,
              help='choco template module cache path: (default %(default)r)')
            _('--template_setting.filesystem_checks', action='store_true', default=False,
              help='choco filesystem checks (default %(default)r)')



A configuration file ``example/demo/conf/ap.conf``:

.. code-block:: text

    template_engine = choco

    # choco template settings 
    template_setting {
        module_directory = "./cache" # choco module cache  path, comments it if wanna  disable 
        filesystem_checks = on 
    }


In diffrentent template engines, the configuration  is diffrentent.