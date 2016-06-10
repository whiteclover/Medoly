#!/usr/bin/env python

import os

from medoly import kanon

import blog
from blog.sqla import SQLABoot


@kanon.boot()
class SiteBoot(object):

    def config(self, options):
        """Setting base site config
        """
        group = options.group("Service settings")
        _ = group.define
        _('-H', '--server.host', default='localhost', help='The host of the http server (default %(default)r)')
        _('-p', '--server.port', default=8888, help='The port of the http server (default %(default)r)', type=int)
        _('-d', '--debug', help='Open debug mode (default %(default)r)', action='store_true', default=False)
        _('-c', '--config', default='/etc/blog/app.conf', help="config path (default %(default)r)", metavar="FILE")
        _("-v", "--version", help="Show blog version {0}".format(blog.__version__))


@kanon.boot()
class WebBoot(object):

    def config(self, options):
        """Web settings"""
        group = options.group("Web settings")
        _ = group.define
        _('--web.cookie_secret', default="secert_key", help='The secert key for secure cookies (default %(default)r)')

    def setup(self, config, settings):
        """Ensure web settings"""
        config.set("web.xsrf_cookies", True)
        config.set("web.login_url", "/auth/login")


@kanon.boot()
class TemplateBoot(object):
    """Jinja2 template options"""

    def config(self, options):
        """Command-line options"""
        group = options.group("Jinja2 Template settings")
        _ = group.define
        _('--template_setting.cache_path', default=None,
          help=' Template byte cache path (default %(default)r)')
        _('--template_setting.auto_reload', default=False,
          help='Reload the template when template modified (default %(default)r)')


@kanon.boot()
class AssetBoot(object):
    """Asset settings"""

    def config(self, options=None):
        """Command-line options
        """
        dirname = os.path.dirname
        path = dirname(os.path.normpath(__file__))

        group = options.group("Asset settings")
        _ = group.define
        _('--asset.url_prefix', default="/assets/", help='Asset url path prefix: (default %(default)r)')
        _('--asset.path', default=os.path.join(path, "asset"), help='Asset files path (default %(default)r)')


@kanon.boot()
def external_boot():
    """External boot options"""
    return [SQLABoot]
