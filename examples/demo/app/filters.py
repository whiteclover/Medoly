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

LOGGER = logging.getLogger(__name__)


@kanon.hook("on_start_request")
def on_load(req_handler):
    LOGGER.debug("on load req_handler: %s", req_handler)


@kanon.error_page(404)
def not_found(req_handler, code, **kw):
    req_handler.render("404.html", page_title='Not Found')
