#!/usr/bin/env python


import tornado.web

from medoly import kanon
from medoly import anthem


@kanon.menu("/entry/([^/]+)")
class EntryHandler(anthem.Handler):

    entry_thing = kanon.Melos("Entry")

    def get(self, slug):
        entry = self.entry_thing.find_by_slug(slug)
        if not entry:
            raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)


@kanon.menu("/archive")
class ArchiveHandler(anthem.Handler):

    entry_thing = kanon.Melos("thing:Entry")

    def get(self):
        entries = self.entry_thing.list_entries()
        self.render("archive.html", entries=entries)


@kanon.menu("/feed")
class FeedHandler(anthem.Handler):

    entry_thing = kanon.Melos("thing:Entry")

    def get(self):
        entries = self.entry_thing.list_entries(page_size=10)
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


@kanon.menu("/compose")
class ComposeHandler(anthem.Handler):

    entry_thing = kanon.Melos("thing:Entry")

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        entry = None
        if id:
            entry = self.entry_thing.find_by_id(int(id))
        self.render("compose.html", entry=entry)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        entry = self.entry_thing.update_or_create_entry(id, title, text, self.current_user.id)

        self.redirect("/entry/" + entry.slug)
