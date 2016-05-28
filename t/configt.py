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


from medoly.config import ConfigFactory, SelectConfig
from util import conf_path


import unittest


class ConfigTest(unittest.TestCase):

    def test_config_from_file(self):
        config = ConfigFactory.parse_file(conf_path, True).to_select_config()

        self.assertEqual(config.get("server.port"), 8880)
        self.assertEqual(config.get("server"), {
                         "port": 8880, "host": "localhost"})
        self.assertEqual(config.get("server.port1"), None)

    def test_get_list(self):
        conf = """list = [1,66]"""
        config = ConfigFactory.parse(conf)
        self.assertEqual(config.get_int_list("list"), [1, 66])

    def test_get_int(self):
        conf = """port = 123"""
        config = ConfigFactory.parse(conf)
        self.assertEqual(config.get_int("port"), 123)

    def test_get_string(self):
        conf = """host = "localhost" """
        config = ConfigFactory.parse(conf)
        self.assertEqual(config.get_string("host"), "localhost")

    def test_get_float(self):
        conf = """f = 1.25 """
        config = ConfigFactory.parse(conf)
        self.assertEqual(config.get_float("f"), 1.25)


class SelectConfigTest(unittest.TestCase):

    def setUp(self):
        self.config = SelectConfig()
        self.config.set("server.host", "localhost")
        self.config.set("server.port", 80)

    def test_get(self):
        self.assertEqual(self.config.get("server.port"), 80)
        self.assertIsNone(self.config.get("server.not_found"))
        # set default
        self.assertEqual(self.config.get("debug", True), True)

    def test_set(self):
        server_confg = self.config.get("server")
        self.assertEqual(server_confg['host'], 'localhost')
        self.assertEqual(server_confg['port'], 80)
        self.assertEqual(self.config.get("server.port"), 80)

    def test_update(self):
        self.config.set("server.host", "localhost")
        self.config.set("server.port", 80)
        config = {"server": {"host": "host2", "port": 90}, "debug": True}
        self.config.update(config)
        self.assertEqual(self.config.get("debug"), True)
        self.assertEqual(self.config.get("server.host"), "host2")

    def test_in(self):

        self.assertTrue("server" in self.config)
        self.assertFalse("server.not_found" in self.config)

    def test_delete(self):
        self.config.delete("server.port")
        self.assertIsNone(self.config.get("server.port"))
