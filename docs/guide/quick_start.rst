Quick Start
++++++++++++++++

This Documentation will teach you how to build a simple app using medoly.

#. Installing medoly
#. Creating a hello world application
#. Running the application



Install medoly
===================


Requires python 2.7 version, tornado 4.0+, ``mako`` and ``jinja2`` template engine.

You can install Medoly with a single command using pip, type this into your terminal:


.. code-block:: bash
	
	pip install medoly

Develop mode, git clone the project, then move to the proejct directory, type this into your terminal:

.. code-block:: bash

	python setup.py develop


Creating a hello world application
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
