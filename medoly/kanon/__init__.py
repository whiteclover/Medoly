#!/usr/bin/env python

import sys

from .manager import InventoryManager
from ._kanon import Kanon


def __bootstrap():
    """Create and bind a singletion kanon application

    Binding the ``Kanon`` public method in kanon module
    """
    canon = Kanon()
    thismodule = sys.modules[__name__]
    for public_method_key in dir(Kanon):
        if not public_method_key.startswith("_"):
            setattr(thismodule, public_method_key, getattr(canon, public_method_key))


__bootstrap()
