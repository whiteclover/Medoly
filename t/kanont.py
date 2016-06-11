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
from medoly import kanon
from medoly import anthem, muses
from tornado.web import RequestHandler


class InventoryMgrTest(unittest.TestCase):

    def setUp(self):
        self.mgr = kanon.InventoryManager()
        kanon.InventoryManager.set_instance(self.mgr)

    def test_set_instance(self):
        mgr = kanon.InventoryManager()
        invalid_mgr = object()
        kanon.InventoryManager.set_instance(mgr)
        self.assertEqual(id(mgr), id(kanon.InventoryManager.instance()))
        self.assertRaises(TypeError, lambda: kanon.InventoryManager.set_instance(invalid_mgr))

    def test_set_name(self):

        self.mgr.set_app_name("kanon")
        self.assertEqual(self.mgr.app_name, "kanon")

    def test_mount_thing(self):
        @kanon.bloom("thing")
        class DefaultNameThing(object):
            pass

        @kanon.bloom("thing")
        class BlablaService(object):
            pass

        @kanon.bloom("thing", "user")
        class UserService(object):
            pass

        kanon.chant()
        self.assertTrue(isinstance(muses.Thing("DefaultName"), DefaultNameThing))
        self.assertTrue(isinstance(muses.Thing("BlablaService"), BlablaService))
        self.assertTrue(isinstance(muses.Thing("user"), UserService))

    def test_mount_mapper(self):
        # default class postfix name mapper
        @kanon.bloom("mapper")
        class DefaultNameMapper(object):
            pass

        # custom class name mapper
        @kanon.bloom("mapper")
        class BlablaDao(object):
            pass

        # custom mapper key
        @kanon.bloom("mapper", "user")
        class UserDao(object):
            pass

        kanon.chant()
        self.assertTrue(isinstance(muses.Backend("DefaultName"), DefaultNameMapper))
        self.assertTrue(isinstance(muses.Backend("BlablaDao"), BlablaDao))
        self.assertTrue(isinstance(muses.Backend("user"), UserDao))

    def test_mount_model(self):
        # default   model
        @kanon.bloom("model")
        class ModelName(object):
            pass

        # custom model key
        @kanon.bloom("model", "user")
        class UserModel(object):
            pass

        kanon.chant()

        self.assertEqual(muses.Model("ModelName"), ModelName)
        self.assertEqual(muses.Model("user"), UserModel)

    def test_add_route(self):
        # default   model
        @kanon.bloom("model")
        class ModelName(object):
            pass

        # custom class name mapper
        @kanon.bloom("mapper")
        class BlablaDao(object):
            pass

        @kanon.bloom("thing")
        class BlablaService(object):
            pass

        @kanon.menu("/")
        class Index(object):
            mapper = kanon.Melos("mapper:BlablaDao")
            thing = kanon.Melos("BlablaService")

        @kanon.menu("/user")
        class UserPage(RequestHandler):
            pass

        kanon.chant()

        self.assertTrue(isinstance(Index.mapper, BlablaDao))
        self.assertTrue(isinstance(Index.thing, BlablaService))
        handler_class = self.mgr.app_ctx.routes[0].handler_class
        self.assertTrue(issubclass(handler_class, RequestHandler))
        self.assertTrue(issubclass(handler_class, anthem.Handler))
        self.assertTrue(issubclass(self.mgr.app_ctx.routes[0].handler_class, RequestHandler))

    def test_add_chrod(self):

        @kanon.bloom("thing")
        class BlablaService(object):
            pass

        @kanon.chord()
        class UserViewMinx(object):
            thing = kanon.Melos("BlablaService")

            def get_user(self):
                pass

        # custom class name mapper
        @kanon.chord("userCache", bean=True)
        class UserCache(object):
            pass

        @kanon.menu("/")
        class Index(UserViewMinx):
            userCache = kanon.Melos("chord:userCache")

        kanon.chant()

        handler_class = self.mgr.app_ctx.routes[0].handler_class
        self.assertTrue(issubclass(handler_class, RequestHandler))
        self.assertTrue(issubclass(handler_class, anthem.Handler))
        self.assertTrue(issubclass(self.mgr.app_ctx.routes[0].handler_class, RequestHandler))
        self.assertTrue(Index.thing == UserViewMinx.thing)
        self.assertTrue(isinstance(UserViewMinx.thing, BlablaService))
        self.assertTrue(isinstance(Index.userCache, UserCache))
        self.assertTrue(isinstance(UserViewMinx(), muses.Chord("UserViewMinx")))

    def test_route(self):
        class PostIndex(object):
            pass

        class PostView(object):
            pass

        @kanon.route("/post")
        def post_menu(menu):
            menu.connect("", PostIndex)
            menu.connect("/{post_id}", PostView)
            menu.connect("/render", render="post.html")

        kanon.chant()
        handler = self.mgr.app_ctx.routes[0]
        self.assertTrue(issubclass(handler.handler_class, anthem.Handler))
        self.assertEqual(handler.regex.pattern, r"/post$")

        handler = self.mgr.app_ctx.routes[2]
        self.assertTrue(issubclass(handler.handler_class, anthem.RenderHandler))
        self.assertEqual(handler.regex.pattern, r"/post/render$")

    def test_compose_file_module(self):
        kanon.compose("simple_app")
        kanon.chant()
        handler_class = self.mgr.app_ctx.routes[0].handler_class
        self.assertTrue(issubclass(handler_class, RequestHandler))
        self.assertTrue(issubclass(handler_class, anthem.Handler))
        self.assertEqual(muses.Model("Greeting").__name__, "Greeting")

    def test_compose_folder_module(self):
        kanon.compose("app")
        kanon.chant()
        handler_class = self.mgr.app_ctx.routes[0].handler_class
        self.assertTrue(issubclass(handler_class, RequestHandler))
        self.assertTrue(issubclass(handler_class, anthem.Handler))
        self.assertEqual(muses.Model("Greeting").__name__, "Greeting")
        self.assertEqual(muses.Backend("Demo").__class__.__name__, "DemoMapper")
        template_mgr = self.mgr.template_manager
        self.assertEqual(len(template_mgr.template_paths), 1)

        self.assertEqual(template_mgr.ui_support, False)
