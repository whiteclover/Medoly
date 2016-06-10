Simple Blog Service
+++++++++++++++++++++



Development
===========

Fork or download it, then run:

.. code-block:: bash 

    cd examples/blog # the path to the project
    python setup.py develop

Compatibility
=============

Built and tested under Python 2.7 

Setup Database
==============

* create database in mysql:
* then run the mysql schema.sql script in the project directoy schema:

.. code-block:: bash

    mysql -u yourusername -p yourpassword yourdatabase < schema.sql


if your database has not been created yet, log into your mysql first using:

.. code-block:: bash

    mysql -u yourusername -p yourpassword yourdatabase
    mysql>CREATE DATABASE a_new_database_name
    # = you can =
    mysql> USE a_new_database_name
    mysql> source schema\mysql.sql


Run in console
================

Type this in yout terminal:

.. code-block:: bash

    > python blogd -c=conf\app.yaml -d

