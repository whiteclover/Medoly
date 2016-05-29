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


import unittest
from medoly.options import Options


class OptionsTest(unittest.TestCase):

    def setUp(self):
        self.argopt = Options("Demo")
        groupopt = self.argopt.group("Site")
        _ = groupopt.define
        _('-H', '--server.host', default='localhost', help='The host of the http server (default %(default)r)')
        _('-p', '--server.port', default=8888, help='The port of the http server (default %(default)r)', type=int)
        _('-d', '--debug', help='Open debug mode (default %(default)r)', action='store_true', default=False)
        _('--secert_key', default="7oGwHH8NQDKn9hL12Gak9G/MEjZZYk4PsAxqKU4cJoY=", help='The secert key for secure cookies (default %(default)r)')
        _('-c', '--config', default='etc/demo/app.conf', help="config path (default %(default)r)", metavar="FILE")

    def test_options(self):
        config = self.argopt.parse_args(['-p', '80'])
        self.assertEqual(config.debug, False)
        config = vars(config)
        self.assertEqual(config['server.port'], 80)
        self.assertEqual(config['server.host'], "localhost")

    def test_set_defaults_options(self):
        self.argopt.set_defaults(**{"server.host": "host", "debug": True})
        config = self.argopt.parse_args()
        self.assertEqual(config.debug, True)
        config = vars(config)
        self.assertEqual(config['server.port'], 8888)
        self.assertEqual(config['server.host'], "host")
