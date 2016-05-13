

from medoly.config import ConfigFactory
from util import conf_path


import unittest


class ConfigTest(unittest.TestCase):

    def test_config_from_file(self):
        config = ConfigFactory.parseFile(conf_path, True).toSelectConfig()

        self.assertEqual(config.get("server.port"), 8880)
        self.assertEqual(config.get("server"), {
                         "port": 8880, "host": "localhost"})
        self.assertEqual(config.get("server.port1"), None)

    def test_get_list(self):
        conf = """list = [1,66]"""
        config = ConfigFactory.parse(conf)
        self.assertEqual(config.getIntList("list"), [1, 66])

    def test_get_int(self):
        conf = """port = 123"""
        config = ConfigFactory.parse(conf)
        self.assertEqual(config.getInt("port"), 123)

    def test_get_string(self):
        conf = """host = "localhost" """
        config = ConfigFactory.parse(conf)
        self.assertEqual(config.getString("host"), "localhost")

    def test_get_float(self):
        conf = """f = 1.25 """
        config = ConfigFactory.parse(conf)
        self.assertEqual(config.getFloat("f"), 1.25)
