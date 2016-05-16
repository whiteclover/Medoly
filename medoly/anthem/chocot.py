#!/usr/bin/env python


"""Choco Tempatle Engine

Example
--------------

index.html:

.. code::

    This is an UI Page
    <%@ PostView(post_id)/>

ui/post.html:


.. code::

    This is a Post View

    Name: ${post.title}
    Content: ${post.content}

.. code:: python


    def create_ui_container():
        from choco.ui import UIContainer, UIModule
        ui_container = UIContainer(["template/ui"])

        class PostView(UIModule):

            default_template = "post.html"

            def initialize(self):
                self.thing = Thing("Post")

            def render(self, post_id):
                post = self.thing.getByPostId(post_id)
                return {
                    "post": post
                }
        ui_container.put_ui("PostView", PostView)
        return ui_container

    t = lookup.TemplateLookup(directories=["template"], ui_container=create_ui_container())
    t.get_template("index.html").render(post_id=122)

"""

from choco.lookup import TemplateLookup
from tornado.template import Loader


class ChocoTemplateLoader(Loader):
    """Choco Tempatle Engine Loader

    Extends:
        Loader


    :param  list[str] directories: the choco template root paths
    :param  kwargs: the more settings for choco template

    :param UIContainer ui_container: the ui template container (default: {None})
    :param string module_directory: the choco template module cache path (default: {None})
    :param bool filesystem_checks: when ``True`` the choco loader will check the template file and reload the last modify template(default: {False})

    """

    def __init__(self, directories, ui_container=None, module_directory=None, filesystem_checks=False, **kwargs):

        super(ChocoTemplateLoader, self).__init__(directories[0], **kwargs)

        self._lookup = TemplateLookup(directories=directories,
                                      ui_container=ui_container,
                                      filesystem_checks=filesystem_checks,
                                      module_directory=module_directory,
                                      input_encoding='utf-8',
                                      output_encoding='utf-8',
                                      default_filters=['decode.utf8'])

    def _create_template(self, name):
        """The tonado temaple loader load the real tempalte


        :param name: the template path name
        :type name:  string
        :returns: the choco template instance
        :rtype: {Template}
        """
        template = self._lookup.get_template(name)
        template.generate = template.render

        return template
