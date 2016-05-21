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
        for k, v in config.items():
            self.set(k, v)

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

    def __init__(self, root, fallback=None):
        if root.value is None:
            raise AttributeError(" error")
        self.root = root.value  # HoconValue
        self.substitutions = root.substitutions  # List<HoconSubstitution>
        self.fallback = fallback  # Config

    def get_node(self, path):
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

    def get_config(self, path):
        cls = self.__class__
        value = self.get_node(path)
        if self.fallback:
            f = self.fallback.get_config(path)
            if value is None and f is None:
                return None
            if value is None:
                return f
            return cls(HoconRoot(value).with_fallback(f))
        if value is None:
            return None
        return cls(HoconRoot(value))

    def __str__(self):
        if self.root is None:
            return ""
        return str(self.root)

    def to_dict(self):
        return self.root.get()

    def to_select_config(self):
        return SelectConfig(self.root.get())

    def with_fallback(self, fallback):
        if fallback == self:
            raise Exception(" error")
        clone = deepcopy(self)
        current = clone
        while current.fallback:
            current.fallback
        current.fallback = fallback
        return clone

    def has_path(self, path):
        return self.get_node(path) is not None

    def append(self, config, fallback):
        #fallbackConfig = ConfigFactory.parse(fallback)
        return config.with_fallback(fallback)


class Config(BaseConfig):

    def get_bool(self, path, default=False):
        value = self.get_node(path)
        if value is None:
            return default
        return value.get_bool()

    def get_int(self, path, default=0):
        value = self.get_node(path)
        if value is None:
            return default
        return value.get_int()

    def get(self, path, default=None):
        value = self.get_node(path)
        if value is None:
            return default
        return value.get_string()

    get_string = get

    def get_float(self, path, default=0.0):
        value = self.get_node(path)
        if value is None:
            return default
        return value.get_float()

    def get_bool_list(self, path):
        value = self.get_node(path)

        return value.get_bool_list()

    def get_float_list(self, path):
        value = self.get_node(path)

        return value.get_float_list()

    def get_int_list(self, path):
        value = self.get_node(path)

        return value.get_int_list()

    def get_list(self, path):
        value = self.get_node(path)

        return value.get_list()

    def get_value(self, path):
        return self.get_node(path)


class PyConfig(BaseConfig):

    def get(self, path, default=None):
        value = self.get_node(path)
        if value is None:
            return default
        return value.get()

from .hocon import Parser, HoconRoot


class ConfigFactory(object):

    @classmethod
    def empty(cls):
        return cls.parse("")

    @classmethod
    def parse(cls, hocon, func=None, pystyle=False):
        res = Parser.parse(hocon, func, pystyle)
        configCls = PyConfig if pystyle else Config
        return configCls(res)

    @classmethod
    def parse_file(cls, path, pystyle=False):
        with open(path) as f:
            content = f.read()
            return cls.parse(content, pystyle=pystyle)

    @classmethod
    def from_json(cls, jsonObj, pystyle=False):
        import json
        text = json.dumps(jsonObj)
        return cls.parse(text, pystyle)
