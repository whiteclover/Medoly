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

from medoly.kanon.manager import InventoryManager, InventoryExistError


class InvertoryMockObj(object):
    pass


class InventoryManagerTest(unittest.TestCase):

    def setUp(self):
        self.mgr = InventoryManager()

    def test_set_app_name(self):
        self.mgr.set_app_name("test_name")
        self.assertEqual(self.mgr.app_name, "test_name")

    def test_put_chord(self):
        self.mgr.put_chord("chord", InvertoryMockObj)
        self.mgr.put_chord("chord_instance", InvertoryMockObj, bean=True)
        self.assertRaises(InventoryExistError, lambda: self.mgr.put_chord("chord", InvertoryMockObj))
        self.assertEqual(self.mgr.chords['chord'][0], InvertoryMockObj)
        self.assertEqual(self.mgr.chords['chord_instance'][0], InvertoryMockObj)
        self.assertEqual(self.mgr.chords['chord_instance'][1]['bean'], True)

    def test_put_model(self):
        self.mgr.put_model("model", InvertoryMockObj)
        self.assertRaises(InventoryExistError, lambda: self.mgr.put_model("model", InvertoryMockObj))
        self.assertEqual(self.mgr.models['model'], InvertoryMockObj)

    def test_put_thing(self):
        self.mgr.put_thing("thing", InvertoryMockObj)
        self.assertRaises(InventoryExistError, lambda: self.mgr.put_thing("thing", InvertoryMockObj))
        self.assertEqual(self.mgr.things['thing'], InvertoryMockObj)

    def test_put_mapper(self):
        self.mgr.put_mapper("mapper", InvertoryMockObj)
        self.assertRaises(InventoryExistError, lambda: self.mgr.put_mapper("mapper", InvertoryMockObj))
        self.assertEqual(self.mgr.mappers['mapper'], InvertoryMockObj)
