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


"""Medoly Application
=================


Examples::


        app = Appliction(handlers, intialize)

        LOG  = logigng.getLogger(__name__)

        def on_load_session(req_handler):
            LOG.debug("on load session for %s", id(req_handler))

        app.attatch("on_start_request", on_load_session)

        def on_not_found(req_handler, status_code, **kw):
            theme = req_handler.application.config.get('theme', 'default')
            tpl = 'theme/' + theme + '/404.html'
            req_handler.render(tpl, page_title='Not Found')

        app.error_page(404, nof_found)


"""

import tornado.web

from .hook import HookMap


class Application(tornado.web.Application):
    """Medoly Application


    Extends:
        tornado.web.Application

    Variables:
        hookpoints {list} -- hooks points
    """

    # Hook points
    hookpoints = ['on_start_request', 'on_end_request',
                  'before_error_response', 'after_error_response']

    def __init__(self, handlers, intialize, **settings):
        """Init

        [description]

        Arguments:
            handlers {list[RequestHandler]} -- tornado request handers
            intialize {fucntion} -- the initailize function hooks
            **settings {[type]} -- the more tornado application settings
        """
        # error pages, contains the error process handler for the status code
        self.error_pages = {}
        self.hooks = HookMap()
        intialize(self)
        tornado.web.Application.__init__(
            self, handlers, **settings)

    def attach(self, point, callback, failsafe=None, priority=None, **kwargs):
        """Added hook point"""
        if point not in self.hookpoints:
            return
        self.hooks.attach(point, callback, failsafe, priority, **kwargs)

    def error_page(self, code, callback):
        """Status code and error expction hander callback

        Arguments:
            code {int} -- the http status code
            callback {function} -- the fucktion


        callback::

        def on_not_found(request_handler, status_code, **kw):
            theme = request_handler.application.config.get('theme', 'default')
            tpl = 'theme/' + theme + '/404.html'
            request_handler.render(tpl, page_title='Not Found')


        :request_handler: the reqeust handler
        :statuc_code: the status code
        :kw: the more args for the excption handler

        Raises:
            TypeError -- the invalid status code type
        """

        if not isinstance(code, int):
            raise TypeError("code:%d is not int type" % (code))
        self.error_pages[str(code)] = callback
