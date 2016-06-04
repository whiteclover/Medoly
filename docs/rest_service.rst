Building a RESTful Web Service
+++++++++++++++++++++++++++++++


This guide walks you through the process of creating a "hello world" RESTful web service with medoly.


.. note::
    The source code in the meodly ``exmaples/rest_service`` directory.

What you’ll build
===============

You’ll build a service that will accept HTTP GET requests at::


    http://localhost:8080/greeting

and respond with a JSON representation of a greeting:

.. code-block:: json

    {"id":1,"content":"Hello, Guest!"}

You can customize the greeting with an optional name parameter in the query string::

    http://localhost:8080/greeting?name=User

The name parameter value overrides the default value of "Guest" and is reflected in the response:

.. code-block:: json

    {"id":1,"content":"Hello, Guest!"}


Create a model class
============================

Like most Medoly Getting Started guides, you can start from scratch and complete each step, or you can bypass basic setup steps that are already familiar to you. Either way, you end up with working code.


Now that you’ve set up the project and build system, you can create your web service.

Begin the process by thinking about service interactions.

The service will handle GET requests for /greeting, optionally with a name parameter in the query string. The GET request should return a 200 OK response with JSON in the body that represents a greeting. It should look something like this:


.. code-block:: json

    {
        "id": 1,
        "content": "Hello, World!"
    }

The id field is a unique identifier for the greeting, and content is the textual representation of the greeting.

To model the greeting representation, you create a model class. Provide a plain python object with fields, constructors, and json  hook method to get json data:

examples/rest_service/greeting/model.py


.. code-block:: python

    from medoly import kanon


    class Greeting(object):

        def __init__(self, sid, content):
            self.sid = sid
            self.content = content

        def __json__(self):
            return {"id": self.sid, "content": self.content}


.. note::
    As you see in steps below, modely uses  the jsonify method the make a json response, and the object has __json__ method will invoke to get json data.

Create a resource handler
=========================

Now we ceating a anthem handler class  for handler the restfull api request.

exmaples/rest_service/greeting/view.py

.. code-block:: python

    import threading
    from medoly import kanon, anthem
    from .model import Greeting


    @kanon.menu('/greeting')
    class GreetingView(anthem.Handler):

        lock = threading.Lock()
        counter = 1

        def get(self):
            with self.lock:
                self.counter += 1
            name = self.get_argument("name", "Guest")
            self.jsonify(Greeting(self.counter, "Hello, {}!".format(name)))

This handler view is concise and simple, but there’s plenty going on under the hood. Let’s break it down step by step.

The ``@menu``  decorator ensures that HTTP requests to /greeting are mapped to the ``GreetingView`` handler class.

The implementation of the ``get`` method body creates and returns a new Greeting object with id and content attributes based on the next value from the counter, and formats the given name by using the string format template.

A key difference between a traditional tornado ``RequestHandler``， the ``write`` method is just for append string text content, when building RESTful application,  please using ``jsonify`` method to create a json content  http response.


Creating the application bootstrap service
===================================

exmaples/rest_service/service.py

.. code-block:: python

    from medoly import kanon
    import logging
    import tornado.ioloop


    LOG = logging.getLogger('greeting')


    class GreetingService(object):
        """ Greeting boot service"""

        def __init__(self):
            mgr = kanon.inventory_manager()
            mgr.set_app_name("Greeting")
            kanon.compose("greeting")
            self.app = kanon.chant()

        def startup(self):
            """Start up service"""
            try:
                port = self.app.config.get("server.port", 8080)
                host = self.app.config.get("server.host", 'localhost')
                LOG.info("Starting Greeting on %s:%s", host, port)
                self.app.listen(port, host)
                tornado.ioloop.IOLoop.instance().start()
            except KeyboardInterrupt as e:
                self.shutdown()

        def shutdown(self):
            """stop the service"""
            tornado.ioloop.IOLoop.instance().stop()


    if __name__ == "__main__":

        GreetingService().startup()

In constuct method, gets the manager to set the app name, then compose scan the greeting module , call ``chant`` method to build a anthem appliction.

In ``startup`` method try load server setting for appliction config then bootstrap the http service through the current default ``IOLoop`` instance. 

Test the service
==============


Type the command in your terminal as blow:

    python service.py
    
Now that the service is up, visit ``http://localhost:8080/greeting``, where you see:


.. code-block:: json


    {"id":1,"content":"Hello, Guest!"}

Provide a name query string parameter with ``http://localhost:8080/greeting?name=Medoly``. Notice how the value of the content attribute changes from "Hello, World!" to "Hello, Medoly!":

.. code-block:: json

    {"id":2,"content":"Hello, Medoly!"}

Summary
===============

Congratulations! You’ve just developed a RESTful web service with medoly.



