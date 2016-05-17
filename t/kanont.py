import unittest
from medoly import kanon
from medoly import anthem


class TestInventoryMgrTest(unittest.TestCase):

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
        self.assertTrue(isinstance(anthem.Thing("DefaultName"), DefaultNameThing))
        self.assertTrue(isinstance(anthem.Thing("BlablaService"), BlablaService))
        self.assertTrue(isinstance(anthem.Thing("user"), UserService))

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
        self.assertTrue(isinstance(anthem.Backend("DefaultName"), DefaultNameMapper))
        self.assertTrue(isinstance(anthem.Backend("BlablaDao"), BlablaDao))
        self.assertTrue(isinstance(anthem.Backend("user"), UserDao))

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

        self.assertEqual(anthem.Model("ModelName"), ModelName)
        self.assertEqual(anthem.Model("user"), UserModel)
