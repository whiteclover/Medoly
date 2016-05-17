Medoly
+++++++++++



Medoly is a Web Framework, the design is inspried by Spring-boot and Emberjs.

#. mako(choco ) tempalte with  ui module styles
#. mvc and mvvm
#. all tornado  features
#. auto dependency injection
#. flexible config and bootstrap


.. code:: python

    #!/usr/bin/env python

    from medoly import kanon
    import tornado.ioloop


    @kanon.menu("/")
    class Index(object):

        def get(self):
            self.write("hello world!")


    @kanon.error_page(404)
    def on_not_fonud(req_handler, code, **kw):
        req_handler.write("Page not found!")

    if __name__ == "__main__":
        kanon.set_debug()
        app = kanon.chant()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()

