Quick Start
++++++++++++++++

This guide will teach you how to build a simple app using medoly.

#. Installing modely
#. Creating a hello world application
#. Running the application



Install medoly
===================


Requires python 2.7 version, tornado 4.0+ is better (tornado 3.0+) and choco template engine extends on mako tempalte engine.

You can install Modely with a single command using pip, type this into your terminal:


.. code-block:: bash
	
	pip install modely

Develop mode, git clone the project, then cd proejct direcotry, type this into your terminal:

.. code-block:: bash

	python setup.py Develop


Create a hello world application
=====================================

Writing code in file named ``hello.py``.


.. code-block:: python

	from medoly import kanon
	import tornado.ioloop


	@kanon.menu("/")
	class Index(object):

	    def get(self):
	        self.write("Hello World!")


	@kanon.error_page(404)
	def on_not_fonud(req_handler, code, **kw):
	    req_handler.write("Page not found!")

	if __name__ == "__main__":
	    app = kanon.chant()
	    app.listen(8888)
	    tornado.ioloop.IOLoop.current().start()



Running the application
==========================

Type this into your terminal for running the application:


.. code-block:: bash
	
	python hello.py
