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

from medoly import cmd
import unittest

from util import conf_path, yaml_conf


class CmdTest(unittest.TestCase):

    def test_get_file_opt(self):
        c = cmd.Cmd(conf_path)
        config = c.get_file_opt()
        self.assertEqual(config.get("server.port"), 8880)

    def test_get_yaml_file_opt(self):
        c = cmd.Cmd(yaml_conf)
        config = c.get_file_opt()
        self.assertEqual(config.get("server.port"), 8880)

    def test_get_file_opt_not_found(self):
        c = cmd.Cmd("not_found")
        config = c.get_file_opt()
        self.assertEqual(len(config), 0)

    def test_parse_cmd(self):
        c = cmd.Cmd(conf_path)
        config = c.parse_cmd("test", [])
        self.assertEqual(config.get("server.port"), 8880)

    def test_yaml_parse_cmd(self):
        c = cmd.Cmd(yaml_conf)
        config = c.parse_cmd("test", [])
        self.assertEqual(config.get("server.port"), 8880)
