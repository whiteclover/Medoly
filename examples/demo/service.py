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


from medoly import kanon
import logging
import tornado.ioloop


LOG = logging.getLogger('app')


class DemoService(object):
    """ Demo boot service"""

    def __init__(self):
        kanon.compose("app")
        self.log_config("demo")
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


if __name__ == "__main__":

    DemoService().startup()
