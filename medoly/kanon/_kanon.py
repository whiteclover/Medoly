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

"""Kanon builder util"""


class Melos(object):
    """ Melos


    Loads inventory for the class, dependecy injection when the inventory manager  called ``load`` method

    Examples:

    .. code: python

        class Index(object):
            user_thing  = Melos("thing:User")
            # default  is a thing inventory
            post_thing = Melos("Post")

    :param inventory_name: the ":" split inventroy name, Defaults if only have the name, will set to thing inventory
    :type inventory_name: string
    """

    def __init__(self, inventory_name):

        self.inventory_name = inventory_name
        parts = inventory_name.split(":")
        genre = "thing"
        name = ""
        if len(parts) >= 2:
            name = parts[1]
            genre = parts[0]
        else:
            name = parts[0]

        #: the the inventory type, eg: ``thing``, ``model``, ``mapper``
        self.genre = genre

        #: the inventory name
        self.name = name
