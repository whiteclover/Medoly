#!/usr/bin/env python


from medoly import kanon
from medoly import anthem


@kanon.menu("/feed")
class FeedHandler(anthem.Handler):

    feed_thing = kanon.Melos("thing:Feed")

    def get(self):
        feed_data = self.feed_thing.feed_entries()
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", **feed_data)
