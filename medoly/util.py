#!/usr/bin/env python
# Copyright (C) 2016 Medoly
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class lazy_attr(object):
    """Lazy property

    Examples::

        class SessionManager(object):

            @lazy_attr
            def author_thing(self):
                return muses.Thing("Author")
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:  # pragma: no cover
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


def get_class_bases(klass):
    """Getting the base classes excluding the type ``object``"""
    bases = klass.__bases__
    if len(bases) == 1 and bases[0] == object:
        return []
    else:
        return list(bases)


def with_metaclass(meta, bases=(object,)):
    """Mete class"""
    return meta("NewBase", bases, {})
