Access resources in muses and Melos
++++++++++++++++++++++++++++++++++++++


muses
==================
``muses`` is the inventory resources namespace.


.. Note::
     If not found a invetory in muses inventory container, it will raise KeyError exception.



Model
------------------------------------


``Model``  is used to access the model class thats the inventory register as model in in the kanon  ``bloom`` decorator  via the access name .


.. code-block:: python

    from medoly.muses import Model
    user_model = Model("User")



Backend
------------------------------------


You can use ``Backend`` to access the mapper instance thats the inventory register as mapper in the kanon ``bloom`` decorator  via the access name .


.. code-block:: python

    from medoly.muses import Backend
    user_mapper = Backend("User")


Thing
------------------------------------


You can use ``Thing`` to access the thing instance thats the inventory register as thing in the kanon ``bloom``  decorator  via the access name .


.. code-block:: python

    from medoly.muses import Thing
    user_thing = Thing("User")


Chord
------------------------------------


You can use ``Thing`` to access the chord instance or class thats the inventory register  in the kanon ``chord`` decorator via the access name .


.. code-block:: python

    from medoly.muses import Chord
    user_service = Chord("User")


Melos
=============


``Melos`` is a resource lazy loader. you can use Melos in Chord class and Handler, UIModule class.
It will load the inventory resource  in the class variable.


.. code-block:: python

    from medoly.kanon import ui, Melos

    @ui("user.html")
    class UserView(object):

        thing = Melos("User")

        def render(self, uid):
            user = self.thing.find_by_uid(uid)
            return {"user": user}

    @menu("/user.json")
    class UserJsonPage(anthem.Handler):

        thing = Melos("thing:User")

        def get(self):
            uid = int(self.get_argument("uid"))
            user = self.thing.find_by_uid(uid)
            self.jsonify(user)


Defaultly, Melos access the inventory type is `thing`.  the access name uses a colon ``:`` to split inventory type
and inventory name ( eg: "thing:User").

Here are the Inventory types as beblow:


+------------------------+----------------------------------+
|  Inventory Type        |  Inventory identification        |
+========================+==================================+
|  model                 | access the model class inventory |
+------------------------+----------------------------------+
| chord                  |  access the chord inventory      |
+------------------------+----------------------------------+
| mapper                 |  access the mapper inventory     |
+------------------------+----------------------------------+
| thing                  |  access the thing inventory      |
+------------------------+------------+----------+----------+


For examples:

.. code-block:: python

    @menu("/user.json")
    class UserJsonPage(anthem.Handler):

        thing = Melos("thing:User")
        model = Melos("model:User")
        mapper = Melos("mapper:User")
        chord = Melos("chord:User")
