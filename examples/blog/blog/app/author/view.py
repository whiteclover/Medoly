#!/usr/bin/env python

import tornado.escape
from medoly import anthem
from medoly import kanon

from blog.security import session


@kanon.menu("/auth/login")
class AuthLoginHandler(anthem.Handler):

    user_thing = kanon.Melos("Author")

    def get(self):
        # If there are no authors, redirect to the account creation page.
        if not self.user_thing.any_author_exists():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)

    def post(self):
        author = self.user_thing.find_by_email(self.get_argument("email"))
        if not author:
            self.render("login.html", error="email not found")
            return

        if self.user_thing.check_password(author, self.get_argument("password")):
            session.login(self, author)
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="incorrect password")


@kanon.menu("/auth/logout")
class AuthLogoutHandler(anthem.Handler):

    def get(self):
        session.logout(self)
        self.redirect(self.get_argument("next", "/"))


@kanon.menu("/auth/create")
class AuthCreateHandler(anthem.Handler):

    user_thing = kanon.Melos("Author")

    def get(self):
        self.render("create_author.html")

    def post(self):
        if self.user_thing.any_author_exists():
            raise tornado.web.HTTPError(400, "author already created")
        password = self.get_argument("password")
        email = self.get_argument("email")
        name = self.get_argument("name")
        author = self.user_thing.create_author(name, email, password)

        session.login(self, author)
        self.redirect(self.get_argument("next", "/"))
