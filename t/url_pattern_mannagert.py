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

import unittest

from medoly.kanon.manager import URLPatternManager


class URLPatternManagerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mgr = URLPatternManager()

    def test_url_rule(self):
        # any
        url = self.mgr.url("/post/{post_id}")
        self.assertEqual(url, r"/post/(?P<post_id>[^/]+)")

        # int
        url = self.mgr.url("/post/{post_id:int}")
        self.assertEqual(url, r"/post/(?P<post_id>-?\d+)")

        # float
        url = self.mgr.url("/post/{post_id:float}")
        self.assertEqual(url, r"/post/(?P<post_id>-?\d+\.\d+)")

        # normal
        url = self.mgr.url("/post/1")
        self.assertEqual(url, "/post/1")

        # tornado regex rule
        url = self.mgr.url("/post/(?P<post_id>[^/]+)")
        self.assertEqual(url, "/post/(?P<post_id>[^/]+)")
        url = self.mgr.url("/post/([^/]+)")
        self.assertEqual(url, "/post/([^/]+)")
