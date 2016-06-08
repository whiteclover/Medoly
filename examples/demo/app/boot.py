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

"""Boot Settings"""

import os
from medoly.kanon import boot


@boot()
class SiteBoot(object):

    def config(self, options):
        """Setting base site config
        """
        group = options.group("Service settings")
        _ = group.define
        _('-H', '--server.host', default='localhost', help='The host of the http server (default %(default)r)')
        _('-p', '--server.port', default=8888, help='The port of the http server (default %(default)r)', type=int)
        _('-d', '--debug', help='Open debug mode (default %(default)r)', action='store_true', default=False)
        _('-c', '--config', default='etc/demo/app.conf', help="config path (default %(default)r)", metavar="FILE")
        _("-v", "--version", help="Show demo version 0.1")


@boot()
class WebBoot(object):

    def config(self, options):
        """Web settings"""
        group = options.group("Web settings")
        _ = group.define
        _('--web.secert_key', default=None, help='The secert key for secure cookies (default %(default)r)')


@boot()
class TemplateBoot(object):
    """Choco template options"""

    def config(self, options):
        group = options.group("Template settings")
        _ = group.define
        _("--template_engine", default="choco", help="Template engine name")
        _('--template_setting.module_directory', default=None,
          help='choco template module cache path: (default %(default)r)')
        _('--template_setting.filesystem_checks', action='store_true', default=False,
          help='choco filesystem checks (default %(default)r)')


@boot()
class AssetBoot(object):
    """Asset settings"""

    def config(self, options=None):
        dirname = os.path.dirname
        path = dirname(os.path.normpath(__file__))

        group = options.group("Asset settings")
        _ = group.define
        _('--asset.url_prefix', default="/assets/", help='Asset url path prefix: (default %(default)r)')
        _('--asset.path', default=os.path.join(path, "asset"), help='Asset files path (default %(default)r)')
