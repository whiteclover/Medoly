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

from medoly.kanon import boot


@boot()
class SiteBoot(object):

    def config(self, options):
        """Setting base site config
        """
        group = options.group("Service settings")
        _ = group.define
        _('-H', '--server.host', default='localhost', help='The host of the http server (default %(default)r)')
        _('-p', '--server.port', default=8888, help='The port of the http server (default %(default)r)', type=int)
        _('-d', '--debug', help='Open debug mode (default %(default)r)', action='store_true', default=False)
        _('--secert_key', default="7oGwHH8NQDKn9hL12Gak9G/MEjZZYk4PsAxqKU4cJoY=", help='The secert key for secure cookies (default %(default)r)')
        _('-c', '--config', default='./conf/app.conf', help="config path (default %(default)r)", metavar="FILE")
        _("-v", "--version", help="Show demo version 0.1")
