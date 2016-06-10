#!/usr/bin/env python

from medoly import kanon
from medoly.muses import Backend
from blog.security import generate_hashed_passwd


@kanon.bloom("thing")
class AuthorThing(object):

    def __init__(self):
        self.mapper = Backend("Author")

    def find_by_id(self, uid):
        """Find user by user id"""
        return self.mapper.find_by_id(uid)

    def find_by_email(self, email):
        """Find user by user's email"""
        return self.mapper.find_by_email(email)

    def any_author_exists(self):
        """Check any author exist in database"""
        return bool(self.mapper.count())

    def create_author(self, name, email, password):
        """Create user

        :param name: the user name

        :param email: the user email
        :param password: the original password
        :type password: string
        :returns: the new author
        :rtype: Author
        """
        hashed_password = generate_hashed_passwd(password)
        user = self.mapper.create_author(name=name, email=email, hashed_password=hashed_password)
        return user

    def check_password(self, author, password):
        """Check author's login password"""
        return author.hashed_password == generate_hashed_passwd(password, author.hashed_password)
