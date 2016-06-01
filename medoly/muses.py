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

"""Muses is the medoly global namespace contains all the dependecy injection objects"""


def Backend(key):
    """Get backend by bean key

    Arguments:
        key {str} -- backend key

    Returns:
            backend  instacne
    """
    return __backend.get(key)


def Thing(key):
    """Get thing by bean key

    Arguments:
        key {str} -- thing key

    Returns:
            thing instacne
     """
    return __thing.get(key)


def Model(key):
    """Get model by bean key

    Arguments:
            key {str} -- model key

    Returns:
            model instacne
    """
    return __model.get(key)


def Chord(key):
    """Get chord by bean key

    Arguments:
            key {str} -- chord key

    Returns:
            chord instacne
    """
    return __chord.get(key)
