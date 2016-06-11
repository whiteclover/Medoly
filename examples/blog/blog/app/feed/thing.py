#!/usr/bin/env python

from datetime import datetime
from medoly import kanon
from medoly.muses import Backend


@kanon.bloom("thing")
class FeedThing(object):
    """Feed Entry"""

    def __init__(self):
        self.mapper = Backend("Entry")

    def feed_entries(self):
        """Get last feed entries"""
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        entries = self.mapper.list_entries(limit=10)
        if entries:
            updated = max([e.updated for e in entries]).strftime(date_format)
        else:
            updated = datetime.utcnow().strftime(date_format)
        return {"entries": entries, "updated": updated}
