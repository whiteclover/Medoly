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


"""Flash message session Mixin
===================================


How to use
-----------------

.. code:: python


    Exmaple::

        class Index(anthem.Handler):

            def get(self):
                self.flash("User name is invalid", "error")
                self.render("user.html")



template "user.html"::

.. code:: mako

        <div> <h2> Flash message</h2>
                ${flash()}
        </div>
"""

import tornado


class FlashMessagesMixin(object):

    @property
    def messages(self):
        if not hasattr(self, '_messages'):
            messages = self.get_secure_cookie('flash_messages')
            self._messages = []
            if messages:
                self._messages = tornado.escape.json_decode(messages)
        return self._messages

    def flash(self, message, level='error'):
        """Appeding message in flash.

        param message: Str, message info.
        param level: message level enum in ["error", "info", "warnning"].
        """
        if isinstance(message, str):
            message = message.decode('utf8')

        self.messages.append((level, message))
        self.set_secure_cookie(
            'flash_messages', tornado.escape.json_encode(self.messages))

    def get_flashed_messages(self):
        """Get flashed message"""
        messages = self.messages
        self._messages = []
        self.clear_cookie('flash_messages')
        if messages:
            html = '<div class="notifications">\n'
            for category, message in messages:
                html += '<p class="%s">%s</p>\n' % (category, message)
            html += '</div>'
            return html
        return ''
