#!/usr/bin/env python

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
        _("--sqlalchemy.url", default="mysql+mysqldb://blog:blog@localhost/blog", help="sqlalchemy url")
        _("--sqlalchemy.encoding", default="utf-8", help="sqlalchemy encoding (default %(default)r)")
        _("--sqlalchemy.isolation_level", default="READ UNCOMMITTED", help="sqlalchemy isolation level (default %(default)r)")
        _("--sqlalchemy.pool_size", default=10, help="sqlalchemy pool size (default %(default)r)", type=int)
        _("--sqlalchemy.pool_recycle", default=10, help="sqlalchemy pool recycle (default %(default)r)", type=int)
        _("-sqlalchemy.echo", default=False, help="sqlalchemy debug mode (default %(default)r)", type=bool)

    def setup(self, config, settings):
        """Setup sqalchemy engine"""
        global Base, db
        sqla_settings = config.get("sqlalchemy", {}).copy()
        url = sqla_settings.pop("url")

        engine = create_engine(url, ** sqla_settings)
        db.configure(bind=engine)
        Base.metadata.bind = engine
