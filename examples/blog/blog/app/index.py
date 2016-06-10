#!/usr/bin/env python

from medoly import kanon
from medoly import anthem


@kanon.menu("/")
class HomeHandler(anthem.Handler):

    entry_thing = kanon.Melos("thing:Entry")

    def get(self):
        entries = self.entry_thing.list_entries()
        if not entries:
            self.redirect("/compose")
            return
        self.render("home.html", entries=entries)
