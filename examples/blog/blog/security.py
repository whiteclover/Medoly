#!/usr/bin/env python

import bcrypt
import tornado.escape


from medoly import muses
from medoly import util


def generate_hashed_passwd(password, hashed_pass=None):
    """generate salt hashed password

    :param password: the original password
    :type password:  string
    :param hashed_pass: the hashed salt
    """
    hashed_pass = hashed_pass or bcrypt.gensalt()
    return bcrypt.hashpw(tornado.escape.utf8(password), hashed_pass)


class _SessionManager(object):
    """Session Manager"""

    SESSION_KEY = "blogdemo_user"

    @util.lazy_attr
    def author_thing(self):
        """Lazy load author thing"""
        return muses.Thing("Author")

    def load(self, req_handler):
        """Load and set author in request handler"""
        user_id = req_handler.get_secure_cookie(self.SESSION_KEY)
        if not user_id:
            return None
        author = self.author_thing.find_by_id(int(user_id))
        req_handler.current_user = author

    def login(self, req_handlder, author):
        """User login process"""
        req_handlder.set_secure_cookie(self.SESSION_KEY, str(author.id))

    def logout(self, req_handlder):
        """User logout process"""
        req_handlder.clear_cookie(self.SESSION_KEY)

#: The global session manager
session = _SessionManager()
