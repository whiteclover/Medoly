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

from medoly.kanon.manager import TempateMananger, InventoryManager
from medoly.template.impl import chocot


class TemplateMangagerTest(unittest.TestCase):

    def setUp(self):
        self.mgr = TempateMananger()

    def test_put_ui(self):
        class Ui(object):
            pass
        self.mgr.put_ui("ui", Ui)
        self.assertTrue("ui" in self.mgr.uis)

    def test_add_template(self):
        self.mgr.add_template_path("template_path")
        self.assertEqual(self.mgr.template_paths[0], "template_path")

    def test_add_ui_path(self):
        self.mgr.add_ui_path("ui_path")
        self.assertEqual(self.mgr.ui_paths[0], "ui_path")

    def test_create_template_engine(self):
        class Ui(object):
            pass
        self.mgr.add_template_path("template_path")
        self.mgr.add_ui_path("ui_path")
        self.mgr.put_ui("ui", Ui)

        self.mgr.load_template_engine("choco")
        self.assertEqual(self.mgr.ui_support, True)

        engine = self.mgr.create_template_loader(InventoryManager.instance())
        self.assertTrue(isinstance(engine, chocot.ChocoLoader))
