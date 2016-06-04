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


import threading
from medoly import kanon, anthem
from .model import Greeting


@kanon.menu('/greeting')
class GreetingView(anthem.Handler):
    """Gretting view handler"""

    lock = threading.Lock()
    counter = 1

    def get(self):
        """Returns the greeting info"""
        with self.lock:
            self.counter += 1
        name = self.get_argument("name", "Guest")
        self.jsonify(Greeting(self.counter, "Hello, {}!".format(name)))
