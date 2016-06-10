#!/usr/bin/env python

from medoly import kanon
from medoly.muses import Model
from sqlalchemy import func

from blog.sqla import db


@kanon.bloom("mapper")
class AuthorMapper(object):

    def __init__(self):
        self.model = Model("Author")

    def find_by_id(self, uid):
        """Find user by user id"""
        return db.query(self.model).get(uid)

    def find_by_email(self, email):
        """Find user by user's emai;"""
        return db.query(self.model).filter(self.model.email == email).first()

    def create_author(self, name, email, hashed_password):
        """Create user

        :param name: the user name

        :param email: the user email
        :param hashed_password: the hashed password
        :type hashed_password: string
        :returns: the new author
        :rtype: Author
        """
        user = self.model(name=name, email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        return user

    def save(self, user):
        """Save user"""
        db.add(user)
        db.commit()

    def count(self):
        """Returns the author count size"""
        return db.query(func.count(self.model.id)).scalar()
