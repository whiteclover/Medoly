``medoly.kanon`` -- The Application Composer
==========================


Kanon
~~~~~~~~~~

.. automodule:: medoly.kanon
    :members:


.. automodule:: medoly.kanon._kanon
    :members:

Composer
~~~~~~~~~~

.. automodule:: medoly.kanon.composer
    :members:

Manager
~~~~~~~~~~~


.. automodule:: medoly.kanon.manager


    InventoryManager
    -------------------------
    .. autoclass:: InventoryManager



    .. automethod:: InventoryManager.instance
    .. automethod:: InventoryManager.set_instance
    .. automethod:: InventoryManager.initilaize_app
    .. automethod:: InventoryManager.load_melos
    
    .. automethod:: InventoryManager.connect
    .. automethod:: InventoryManager.add_route
    .. automethod:: InventoryManager.put_model
    .. automethod:: InventoryManager.put_mapper
    .. automethod:: InventoryManager.put_thing
    .. automethod:: InventoryManager.put_chord
    .. automethod:: InventoryManager.put_boot

    .. automethod:: InventoryManager.mount_model
    .. automethod:: InventoryManager.mount_mapper
    .. automethod:: InventoryManager.mount_thing
    .. automethod:: InventoryManager.mount_chord
    .. automethod:: InventoryManager.mount_menu


    Error
    ---------------------

    .. autoclass:: InventoryExistError
        :members:

    App context 
    ---------------------
    .. automodule:: medoly.kanon.ctx
        :members:


    Menu
    ------------

    .. autoclass:: Menu

    TemplateManager
    --------------------------

    .. autoclass:: TempateMananger


    .. automethod:: TempateMananger.is_valid
    .. automethod:: TempateMananger.put_ui
    .. automethod:: TempateMananger.create_template_loader
    .. automethod:: TempateMananger.add_ui_path
    .. automethod:: TempateMananger.add_template_path

    URLPatternManager
    --------------------------

    .. autoclass:: URLPatternManager
    .. automethod:: URLPatternManager.add_pattern
    .. automethod:: URLPatternManager.url
