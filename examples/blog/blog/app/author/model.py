#!/usr/bin/env python

from medoly import kanon
from sqlalchemy import (Column, Integer, String,)

from blog.sqla import Base


@kanon.bloom("model")
class Author(Base):
    """Author model """

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False)

    def __repr__(self):
        return "<Author('%s')>" % (self.name)
