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


LOG = logging.getLogger('greeting')


class GreetingService(object):
    """ Greeting boot service"""

    def __init__(self):
        """Get the manager setting the app name, then compose scan a app module , 
        call ``chant`` method to build a anthem appliction.
        """
        mgr = kanon.inventory_manager()
        mgr.set_app_name("Greeting")
        kanon.compose("greeting")
        self.app = kanon.chant()

    def startup(self):
        """Start up service"""
        try:
            # try get server config for app config
            port = self.app.config.get("server.port", 8080)
            host = self.app.config.get("server.host", 'localhost')
            LOG.info("Starting Greeting on %s:%s", host, port)
            self.app.listen(port, host)
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt as e:
            self.shutdown()

    def shutdown(self):
        """Stop the service"""
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":

    GreetingService().startup()
