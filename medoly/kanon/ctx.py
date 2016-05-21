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


class AppContext(object):
    """The application context
    """

    def __init__(self):
        #: the requet handler hook entries
        self.hooks = []

        #: the reuqest handler classes
        self.routes = []

        #: the athem apllcation config settings
        self.settings = {}

        #: the error exception handler hook callbacks
        self.error_pages = {}

    def attach(self, point, callback, failsafe, priority, kwargs):
        self.hooks.append((point, callback, failsafe, priority, kwargs))

    def error_page(self, status_code, callback):
        self.error_pages[status_code] = callback

    def extend_routes(self, routes):
        self.routes.extend(routes)
