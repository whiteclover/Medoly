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


import os
import unittest
import util

from tornado.template import Template
from medoly.template import engine
from medoly.template.impl import chocot, selene


class TeplateEngineTest(unittest.TestCase):

    def init_template(self, name):
        self.template = engine.TemplateEngine(name)
        self.template_loader = self.template.create_template_loader([util.template_path])

    def base_template_test(self, name):
        self.init_template(name)
        t = self.template_loader.load(name + ".html")
        text = t.generate(name=name)
        self.assertIn(name, text)

    def test_mako(self):
        self.base_template_test("mako")
        self.assertEqual(self.template.ui_support, False)
        self.assertEqual(self.template.name, "makot")

    def test_choco(self):
        self.base_template_test("choco")
        self.assertEqual(self.template.name, "chocot")

    def test_selene(self):
        self.base_template_test("selene")
        self.assertEqual(self.template.ui_support, True)
        self.assertEqual(self.template.name, "selene")

    def test_jinja2(self):
        self.base_template_test("jinja2")
        self.assertEqual(self.template.ui_support, False)
        self.assertEqual(self.template.name, "jinja2t")

    def test__import_template_classes(self):
        classes = engine._import_template_classes("medoly.template.impl.chocot", "choco")
        self.assertEquals(classes, [chocot.ChocoLoader, chocot.UIContainer, chocot.UIModule])

    def test_not_find_template_adapter(self):
        self.assertRaises(NotImplementedError, lambda: engine.TemplateEngine("bad_adapter"))


class User(object):

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name


class UserView(selene.UIModule):

    default_template = "user.html"

    def render(self, uid):
        return {"user": User(uid, "Medoly")}


class SeleneTemplateTest(unittest.TestCase):

    def setUp(self):
        template_path = os.path.join(util.template_path, "selene")
        self.ui_container = ui_container = selene.UIContainer([os.path.join(template_path, "ui")])

        ui_container.put_ui("UserView", UserView)
        self.loader = selene.SeleneLoader([template_path], ui_container=ui_container)
        self.loader.namespace['handler'] = True

    def test_render(self):
        t = self.loader.load("user_index.html")
        text = t.generate(name="Selene", uid=12)
        self.assertIn("Hello Selene", text)
        self.assertIn("<p> Name: Medoly</p>", text)

    def test_ui_contanier(self):
        self.assertEqual(self.ui_container.get_ui("UserView"), UserView)
        mod = self.ui_container.get_template("user.html")
        self.assertTrue(isinstance(mod, Template))

    def test_not_found_template(self):
        self.assertRaises(selene.errors.TopLevelLoaderException,
                          lambda: self.loader.load("not_found"))

    def test_not_found_ui(self):
        self.assertRaises(selene.errors.TopLevelLoaderException,
                          lambda: self.ui_container.get_template("not_found"))

    def test_patch(self):
        import tornado.template
        selene.patch.patch_tornado_template()
        self.assertEqual(tornado.template._Module, selene.patch._Module)
