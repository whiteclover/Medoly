Medoly
+++++++++++



Medoly is a Web Framework, the design is inspried by Spring-boot and Emberjs.

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
        app = kanon.chant()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()


.. note::
    More examples see ``examples`` directory.

