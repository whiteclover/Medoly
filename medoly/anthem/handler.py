#!/usr/bin/env python
#
# Copyright 2016 Medoly
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from tornado.web import RequestHandler, url
from tornado.escape import utf8, json_encode


from .flash import FlashMessagesMixin


class Handler(RequestHandler, FlashMessagesMixin):
    """Medoly Request Hander class

    Extends:
        RequestHandler
        FlashMessagesMixin
    """

    def prepare(self):
        """Perpare request process

        [description]
        """
        self.hooks.run('on_start_request', self)
        self.on_start_request()

    def on_start_request(self):
        """Process hook after ``on_start_request''
        """
        pass

    def get_current_user(self):
        """Override to determine the current user from, e.g., a cookie."""
        return None

    @property
    def current_user(self):
        """The authenticated user for this request.

        This is a cached version of `get_current_user`, which you can
        override to set the user based on, e.g., a cookie. If that
        method is not overridden, this method always returns None.

        We lazy-load the current user the first time this method is called
        and cache the result after that.
        """
        if not hasattr(self, "account"):
            self.account = self.get_current_user()
        return self.account

    @current_user.setter
    def current_user(self, value):
        self.account = value

    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.
        May be overridden by subclasses to add or modify values.
        The results of this method will be combined with additional
        defaults in the `tornado.template` module and keyword arguments
        to `render` or `render_string`.
        """
        namespace = dict(
            handler=self,
            flash=self.get_flashed_messages,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            pgettext=self.locale.pgettext,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url
        )
        return namespace

    def jsonify(self, json_obj):
        """Json data write

        Arguments:
            json_obj {object} -- the data can json encoding

        Raises:
            RuntimeError --  run time exception when  request had finshed
        """
        if self._finished:
            raise RuntimeError("Cannot jsonify() after finish().  May be caused "
                               "by using async operations without the "
                               "@asynchronous decorator.")
        chunk = json_encode(json_obj)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        chunk = utf8(chunk)
        self._write_buffer.append(chunk)

    def render(self, template_name, **kwargs):
        """Renders the template with the given arguments as the response."""
        html = self.render_string(template_name, **kwargs)
        self.finish(html)

    def on_finish(self):
        """Hook  pointer process  on request finshing
        """
        self.hooks.run('on_end_request', self)
        self.on_end_request()

    def on_end_request(self):
        """Custom request hanlder hook on end request
        """
        pass

    def Backend(self, key):
        """Get backend by bean key

        Arguments:
            key {str} -- backend key

        Returns:
             backend instacne
        """
        return __backend.get(key)

    def Thing(self, key):
        """Get thing by bean key

        Arguments:
            key {str} -- thing key

        Returns:
             thing instacne
        """
        return __thing.get(key)

    def Model(self, key):
        """Get model by bean key

        Arguments:
            key {str} -- model key

        Returns:
             model instacne
        """
        return __model.get(key)


class RenderHandler(Handler):
    """Render Hanlder class """

    def initialize(self, template):
        """Initialize and bind tempalte


        Arguments:
            template {str} -- tempalte path
        """
        self.template = template

    def get(self, *args):
        """Reder template
        """
        self.render(self.template)


def Backend(key):
    return __backend.get(key)


def Thing(key):
    return __thing.get(key)


def Model(key):
    return __model.get(key)
