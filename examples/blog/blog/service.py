#!/usr/bin/env python

import logging
import tornado.ioloop


from medoly import kanon


LOG = logging.getLogger(__name__)


class BlogService(object):
    """ Blog boot service"""

    def __init__(self):
        kanon.compose("blog.app")
        self.log_config("blog")
        self.app = kanon.chant()

    def log_config(self, tag):
        """log config"""
        format = tag + '[%%(process)d]: [%%(levelname)s] %s%%(message)s' % '%(name)s - '
        logging.basicConfig(format='[%(asctime)s] ' + format, datefmt='%Y%m%d %H:%M:%S', level=logging.DEBUG)

    def startup(self):
        """Start up service"""
        try:
            port = self.app.config.get("server.port", 8888)
            host = self.app.config.get("server.host", 'localhost')
            LOG.info("Starting demo on %s:%s", host, port)
            self.app.listen(port, host)
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt as e:
            self.shutdown()

    def shutdown(self):
        """Stop the service"""
        tornado.ioloop.IOLoop.instance().stop()
