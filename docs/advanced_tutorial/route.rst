More about routing
=================

The kanon ``menu`` decorator links a url path to a  request handler class. it supports the regex expression dynamic route. 
However, the kanon has a  url perprocess rule for url route.


Dynamic route
~~~~~~~~~~~~~~~~~

The url supports preprocessing rule for building dynamic path arguement variable, it processes the simple name enclosed in braces (like. ``{post_id}``) to an path  arguement variable in regex expression url path.

Examples::
    
    /{post_id} #=> /(?P<name>[^/]+)
    /post/{category}/{page_id} #=> /post/(?P<category>[^/]+)/(?P<page_id>[^/]+)


Optionally, it can be used by specifying a rule with {name:filter}. Here are the rules:

:int: matches integer number.
:float: similar to ``int`` but for decimal numbers.

Example:

.. code-block:: python

    @kanon.menu('/posts/{post_id:int}')
    class PostView(anthem.Handler):

        def get(self, post_id):
            post_id = int(post_id)
            self.write({"post_id":  post_id})


Link handler with ``route`` decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


In kanon has an other decorator ``route``  supports to link a group handlers to url paths at once.


Example:


.. code-block:: python

    @kanon.route("/post") # url prefix
    def post_menu(menu):
        menu.connect("/", PostIndexPage) # /post/
        menu.connect("/{post_id:int}",  PostPageView) # /post/{post_id}

It  creates a ``Connector`` and passed it in ``post_menu`` function, calls the ``connect`` method to link to handlers.


connect
-----------------

    .. automodule:: medoly.kanon.composer
    .. automethod:: Connector.connect