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

"""
The tornado methods or functions patch  module
"""

import traceback
import datetime
import decimal

try:
    import simplejson as json  # try external module
except ImportError:
    import json

__all__ = ('patch_tornado', 'as_json', 'hooks', 'json_encode', 'write_error')


def as_json(obj):
    """Returns the json serialize content

    When the ``obj`` is a class object instance and has ``__json__`` method, then it will call the method,
    and dumps the return content. Also it can handle the datetime.date and decimal dumps
    """
    if hasattr(obj, '__json__') and callable(obj.__json__):
        return obj.__json__()
    if isinstance(obj, (datetime.date,
                        datetime.datetime,
                        datetime.time)):
        return obj.isoformat()[:19].replace('T', ' ')
    elif isinstance(obj, (int, long)):
        return int(obj)
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")


def json_encode(value, ensure_ascii=True, default=as_json):
    """Returns the json serialize stream"""
    return json.dumps(value, default=default, ensure_ascii=ensure_ascii)


def write_error(self, status_code, **kwargs):
    """Handle the last unanticipated exception. (Core)"""
    try:
        self.hooks.run("before_error_response",
                       self, status_code, **kwargs)
        handler = self.application.error_pages.get(str(status_code), None)
        if handler:
            handler(self, status_code, **kwargs)
        else:
            if self.settings.get("serve_traceback") and "exc_info" in kwargs:
                # in debug mode, try to send a traceback
                self.set_header('Content-Type', 'text/plain')
                for line in traceback.format_exception(*kwargs["exc_info"]):
                    self.write(line)
                self.finish()
            else:
                self.finish("<html><title>%(code)d: %(message)s</title>"
                            "<body>%(code)d: %(message)s</body></html>" % {
                                "code": status_code,
                                "message": self._reason,
                            })
    finally:
        self.hooks.run("after_error_response", self, status_code, **kwargs)


@property
def hooks(self):
    """Get Application request handler hooks"""
    return self.application.hooks


def patch_tornado():
    """Patch tornado

    Here are the methods or fucntions are patched :

     :web.RequestHandler.write_error: ``medoly.anthem.pathc.write_error``
     :web.RequestHandler.hooks: ``medoly.anthem.pathc.hooks``
     :escape.json_encode:  ``medoly.anthem.pathc.json_encode``

    """

    from tornado import escape
    from tornado import web
    web.RequestHandler.write_error = write_error
    web.RequestHandler.hooks = hooks
    escape.json_encode = json_encode
