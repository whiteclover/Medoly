Medoly
+++++++++++



Medoly is a Web Framework inspried by Spring and Emberjs desgin.

#. Auto-custom mako template
#. Flexible ioc manager



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
