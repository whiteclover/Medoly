A  Blog Service with SQLAlchemy
++++++++++++++++++++++++++++++++++++++++++


This Guide will teach you to build a simple blog service, using the  fully ``MVC`` design and integrating  the SQLAlchemy to access database.

Introduction
=================

This simple blog app has an author entity and entry entity. It has two main features as below:

#. Post entry  list page
#. Post show page
#. Post edit page
#. A simple user system to login, logout and register a author.


.. note::
    The source code in the medoly ``examples/blog`` directory.

Setup the project
====================


python project uses the ``setup.py`` to package the  python project, Here is the this deom setup.py as below:


examples/blog/setup.py

.. code-block:: python

    #!/usr/bin/env python

    import os
    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    import blog


    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

    setup(name='blog',
          version=blog.__version__,
          description='Blog is simple blog demo wrote by Medoly',
          long_description=readme,
          packages=['blog'],
          install_requires=['medoly', 'sqlalchemy', 'markdown', 'bcrypt'],
          license="Apache License",
          platforms='any'
          )

The demo requires the ``sqlalchemy`` an orm module to access  MySQL service, ``markdown`` for build markdown content and bcrypt to encrypt author password . Type this into your terminal for installing them:

.. code-block:: bash

  pip insall SQLAlchemy
  pip insall markdown
  pip bcrypt


Integrating SQLAlchemy
==========================

Creating a global sqlalchemy scoped session named ``db`` and the  declarative base named ``Base``.
SQLABoot class is used  to configure command-line options and boot sqalchemy engine.


examples/blog/blog/sqla.py

.. code-block:: python

  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import (
      scoped_session,
      sessionmaker,
  )
  from sqlalchemy import create_engine

  #: the sqlalchemy scoped session
  db = scoped_session(sessionmaker())

  #: the sqla  declarative base
  Base = declarative_base()


  class SQLABoot(object):

      def config(self, options):
          """Setting sqlalchemy config"""
          group = options.group("SQLAlchemy settings")
          _ = group.define
          _("--sqlalchemy.url", default=None, help="sqlalchemy url")
          _("--sqlalchemy.encoding", default="utf-8", help="sqlalchemy encoding (default %(default)r)")
          _("--sqlalchemy.pool_size", default=10, help="sqlalchemy pool size (default %(default)r)", type=int)
          _("--sqlalchemy.pool_recycle", default=10, help="sqlalchemy pool recycle (default %(default)r)", type=int)
          _("--sqlalchemy.echo", default=False, help="sqlalchemy debug mode (default %(default)r)", type=bool)

      def setup(self, config, settings):
          """Setup sqalchemy engine"""
          global Base, db
          sqla_settings = config.get("sqlalchemy", {}).copy()
          url = sqla_settings.pop("url")

          engine = create_engine(url, ** sqla_settings)
          db.configure(bind=engine)
          Base.metadata.bind = engine

.. note::

  It is the service has a database sqalchemy engine to access the database, not the ``tornado.Application`` has a database access instance. keep the application to be clear, not includes every thing in it.

  Keep the principle:

  Medoly keeps the ``Singleton Pattern Design`` as a gold principle to ``Integrate`` the third-party modules in the top level service namespace . Don't bind every thing in the application (``tornado.Application``) instance. Just keep a global ``singleton`` instance in the service namespace.


Create the model classes
==========================
