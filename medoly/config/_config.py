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

"""Human-Optimized Config Object Notation
"""


from copy import deepcopy


class SelectConfig(object):
    """Select dict configuration tool

      Example:

        >>> conf = SelectConfig()
        >>> conf.set("db.host", "localhost")
        >>> conf.get("db")
        ...       {"host": "localhost"}
        >>> conf.get("db.host")
        ...     "localhost"

    :param config: the default dict namnesapce for config, defaults to None
    :type config: dict, optional
    """

    def __init__(self, config=None):
        self._config = config or dict()

    def __len__(self):
        return len(self._config)

    def set(self, key, value):
        """Set a chain key  value

        :param key: the config chain key with dot split, like "db.host", "host"
        :type key: string
        :param value: the value for key store
        """
        keys = self._keys(key)
        config = self._config
        i = 0
        for k in keys:
            if isinstance(config, dict) and k in config:
                if i == len(keys) - 1:
                    config[k] = value
                    return
                config = config[k]
                i += 1

        keys = keys[i:]
        last_key = keys.pop()
        for k in keys:
            config[k] = {}
            config = config[k]
        config[last_key] = value

    def get(self, key=None, default=None):
        """Get the chain key value, if not fond returns the default value

        :param key: the key. defaults to None, returns the root config.
        :type key: string, optional
        :param default: the default value when not found the key, defaults to None
        :returns: the value for the chain key
        """
        keys = self._keys(key)
        config = self._config
        for k in keys:
            if k in config:
                config = config[k]
            else:
                config = default
                break

        return config

    def delete(self, key):
        """Remove the key config from the current config"""
        keys = self._keys(key)
        if len(keys) == 2:
            v = self.get(keys[0])
            if isinstance(v, dict):
                del v[keys[1]]
        else:
            del self._config[keys[0]]

    def update(self, config):
        """Update the settings in the current config"""
        for k, v in config.items():
            self.set(k, v)

    def config(self):
        """Return real dict config """
        return self._config

    def __contains__(self, key):
        """Check a key in the config"""
        keys = self._keys(key)
        contains = True
        config = self._config
        for k in keys:
            if k in config:
                config = config[k]
            else:
                contains = False
                break

        return contains

    def _keys(self, key):
        """Split the dot chain key to list"""
        return key.split('.')

    def __json__(self):
        return self._config


class BaseConfig(object):
    """Base Config

    :param root:  the real hocon root value
    :type root: HoconRoot
    :param fallback:  the fallback for handle hocon actions, defaults to None
    :raises: AttributeError
    """

    def __init__(self, root, fallback=None):

        if root.value is None:
            raise AttributeError(" error")
        self.root = root.value  # HoconValue
        self.substitutions = root.substitutions  # List<HoconSubstitution>
        self.fallback = fallback  # Config

    def get_node(self, path):
        """Gets the path data node"""
        keys = path.split(".")
        current_node = self.root
        if current_node is None:
            raise KeyError("Doesn't exist the key:" % (path))
        for key in keys:
            current_node = current_node.get_childe_object(key)
            if current_node is None:
                if self.fallback:
                    return self.fallback.get_node(path)
                return None
        return current_node

    def __str__(self):
        if self.root is None:
            return ""
        return str(self.root)

    def to_dict(self):
        """Converts to dict"""
        return self.root.get()

    def to_select_config(self):
        """Converts to SelectConfig"""
        return SelectConfig(self.root.get())

    def with_fallback(self, fallback):
        """Clones a new one config"""
        if fallback == self:
            raise Exception(" error")
        clone = deepcopy(self)
        current = clone
        while current.fallback:
            current.fallback
        current.fallback = fallback
        return clone

    def has_path(self, path):
        """Check  the config has the path node"""
        return self.get_node(path) is not None


class Config(BaseConfig):

    def get_bool(self, path, default=False):
        """Gets the bool data value, defaults not found returns the default value"""
        value = self.get_node(path)
        if value is None:
            return default
        return value.get_bool()

    def get_int(self, path, default=0):
        """Gets the integer data value, defaults not found returns the default value"""
        value = self.get_node(path)
        if value is None:
            return default
        return value.get_int()

    def get(self, path, default=None):
        """Gets the  string data value, defaults not found returns the default value"""
        value = self.get_node(path)
        if value is None:
            return default
        return value.get_string()

    get_string = get

    def get_float(self, path, default=0.0):
        """Gets the  float data value, defaults not found returns the default value"""
        value = self.get_node(path)
        if value is None:
            return default
        return value.get_float()

    def get_bool_list(self, path):
        """Gets the  bool data value, defaults not found returns the default value"""
        value = self.get_node(path)

        return value.get_bool_list()

    def get_float_list(self, path):
        """Gets the  float list data value"""
        value = self.get_node(path)

        return value.get_float_list()

    def get_int_list(self, path):
        """Gets the  int list data value"""
        value = self.get_node(path)

        return value.get_int_list()

    def get_list(self, path):
        """Gets the  list ojbect data value"""
        value = self.get_node(path)

        return value.get_list()

    def get_value(self, path):
        """Gets the  string data node, defaults not found returns the default value"""
        return self.get_node(path)


class PyConfig(BaseConfig):

    def get(self, path, default=None):
        """Get real type value"""
        value = self.get_node(path)
        if value is None:
            return default
        return value.get()

from medoly.config.hocon import Parser


class ConfigFactory(object):

    @classmethod
    def empty(cls):
        """Creates a empty hocon config"""
        return cls.parse("")

    @classmethod
    def parse(cls, hocon, func=None, pystyle=False):
        """Parses and creates a hocon config from  text string"""
        res = Parser.parse(hocon, func, pystyle)
        configCls = PyConfig if pystyle else Config
        return configCls(res)

    @classmethod
    def parse_file(cls, path, pystyle=False):
        """Parses and creates a hocon confi from  the file path"""
        with open(path) as f:
            content = f.read()
            return cls.parse(content, pystyle=pystyle)

    @classmethod
    def from_json(cls, jsonObj, pystyle=False):
        """Creates hocon from json data"""
        import json
        text = json.dumps(jsonObj)
        return cls.parse(text, pystyle)
