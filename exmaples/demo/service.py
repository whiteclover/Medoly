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

import tornado.ioloop


class DemoService(object):

    def __init__(self):
        kanon.set_app_name("Demo")
        kanon.set_debug()
        kanon.compose("app")
        self.app = kanon.chant()

    def startup(self):
        try:
            port = 8888
            host = 'localhost'
            self.app.listen(port, host)
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt as e:
            self.shutdown()

    def shutdown(self):
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":

    DemoService().startup()
