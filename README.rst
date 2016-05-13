Medoly
+++++++++++



Medoly is a Web Framework, the design is inspried by Spring-boot and Emberjs.

#. mako(choco ) tempalte with  ui module styles
#. mvc and mvvm
#. all tornado  features
#. auto dependency injection
#. flexible config and bootstrap


.. code:: python


	class DemoService(object):

	    def __init__(self):
	        kanon.set_app_name("Demo")
	        kanon.set_debug()
	        kanon.compose("app")
	        self.app = kanon.chant()

	    def startup(self):
	        try:
	            port = 8888
	            host = 'localhost'
	            self.app.listen(port, host)
	            tornado.ioloop.IOLoop.instance().start()
	        except KeyboardInterrupt as e:
	            self.shutdown()

	    def shutdown(self):
	        tornado.ioloop.IOLoop.instance().stop()


	if __name__ == "__main__":

	    DemoService().startup()
