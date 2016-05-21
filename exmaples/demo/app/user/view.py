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

from medoly.kanon import menu


@menu("/user")
class UserPage(object):

    def get(self):
        uid = int(self.get_argument("uid"))
        self.render("user_index.html", uid=uid)


@menu("/user.json")
class UserJsonPage(object):

    __thing__ = """thing->User"""

    def get(self):
        uid = int(self.get_argument("uid"))
        user = self.thing.find_by_uid(uid)
        self.jsonify(user)
