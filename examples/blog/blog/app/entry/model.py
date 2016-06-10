#!/usr/bin/env python

from medoly import kanon
from sqlalchemy import (Column, Integer, String,)
from sqlalchemy.dialects.mysql import MEDIUMTEXT, DATETIME, TIMESTAMP

from blog.sqla import Base


@kanon.bloom("model")
class Entry(Base):
    """Entry model"""

    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, nullable=False)
    slug = Column(String(100), nullable=False)
    title = Column(String(512), nullable=False)
    markdown = Column(MEDIUMTEXT, nullable=False)
    html = Column(MEDIUMTEXT, nullable=False)
    published = Column(DATETIME, nullable=False)
    updated = Column(TIMESTAMP, nullable=False, index=True)

    def __repr__(self):
        return "<Entry(id: %s, title: %s)>" % (self.id, self.title)
