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


"""Console option  parser
"""
import os
import sys

from medoly import options
from medoly.config import SelectConfig, ConfigFactory

import logging

LOG = logging.getLogger(__name__)


class Null(object):
    """Null instaince for parsing hocon and Option config
    """
    pass

# Null singleton
_Null = Null()


class Cmd(object):
    """Termial options parse and config util tool
    """

    def __init__(self, config_path, opt=None):
        """Init

        :param string config_path: hocon config file path
        :param Options opt: the default option config class instance
                (default: {None}, use the global default options instance)
        """
        self.options = opt or options
        self.confing_path = config_path

    def get_file_opt(self):
        """Loading the hocon config for the file path

        Returns:
            SelectDict -- the option select dict config
        """
        # parse terminal option get file path, then load the hocon from file path
        opt = options.Options(None)
        opt.define('-c', '--config', default=self.confing_path,
                   help="config path (default %(default)r)", metavar="FILE")
        o = opt.parse_args(sys.argv)
        return config_from_file(o.config)

    def parse_cmd(self, help_doc, boots):
        """Parse config and setting config for the terminal options

        Try load config from configuration file path, then override the file config by the command options .

        :param string help_doc: The OptionPaser help doc
        :param boots:  the boot  instances options

        Returns:
            SelectConfig --  the dict like config
        """
        self.options.setup_options(help_doc)
        self.boot_options(self.options, boots)
        file_config = self.get_file_opt()
        self._set_defaults(file_config, boots)
        opt = self.options.parse_args()
        config = SelectConfig()
        config.update(file_config.config())
        config.update(vars(opt))
        return config

    def boot_options(self, opt, boots):
        """Boot terminal option
        """
        for boot in boots:
            if hasattr(boot, 'config'):
                boot.config(opt)

    def _set_defaults(self, file_config, boots):
        """Setting the default option config
        """

        opt = options.Options(None)
        self.boot_options(opt, boots)

        opt = opt.parse_args()
        d = {}
        config = vars(opt)
        for k in config:
            v = file_config.get(k, _Null)
            if v != _Null:
                d[k] = v
        self.options.set_defaults(**d)


def config_from_file(path):
    """Load config form file

    If config path exist  try to load and parse the config the file, else returns a empty config.
    If the config path extension is ``yml`` , will load the config by yaml parse module requires
    the yaml module, otherwise load hocon config
    """
    if os.path.exists(path):
        # try load yaml config
        if path.endswith(".yaml"):
            yaml_config = _get_yaml_config(path)
            config = SelectConfig()
            config.update(yaml_config)
            return config
        else:
            config = ConfigFactory.parse_file(path, pystyle=True)
            return config.to_select_config()

    # Returns default empty config
    return SelectConfig()


def _get_yaml_config(path):
    """Try load yaml from the path

    :param string path: the yaml file path
    """
    try:
        import yaml
    except ImportError as e:
        LOG.warning("Yaml config requires pyyaml modlule.")
        raise e
    with open(path) as f:
        return yaml.safe_load(f)
