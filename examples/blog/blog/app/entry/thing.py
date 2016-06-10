#!/usr/bin/env python


import markdown
import tornado.web
import re
import unicodedata


from medoly import kanon
from medoly.muses import Backend


@kanon.bloom("thing")
class EntryThing(object):
    """Entry logic layer"""

    def __init__(self):
        self.mapper = Backend("Entry")

    def find_by_id(self, entry_id):
        """Find entry by entry id"""
        return self.mapper.find_by_id(entry_id)

    def list_entries(self, page_no=1, page_size=5):
        """List entry page

        :param  int page_no: the page number, defaults to 0
        :param int page_size: the page size, defaults to 10

        :returns: list[Entry]
        """
        offset = (page_no - 1) * page_size
        return self.mapper.list_entries(page_size, offset)

    def find_by_slug(self, slug):
        """Find entries by the entry slug

        :param string slug: the entry slug
        :returns: the entries
        :rtype: Entry
        """
        return self.mapper.find_by_slug(slug)

    def update_or_create_entry(self, entry_id, title, text, author_id):
        """Update or create a entry

        If  entry_id is not ``None``, try to update the entry, else create a new entry
        """
        html = markdown.markdown(text)
        if entry_id:
            entry = self.mapper.find_by_id(int(entry_id))
            if not entry:
                raise tornado.web.HTTPError(404)
            slug = entry.slug

            entry.title = title
            entry.html = html
            entry.text = text
            return self.mapper.save(entry)

        else:
            slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug:
                slug = "entry"
            while True:
                e = self.mapper.find_by_slug(slug)
                if not e:
                    break
                slug += "-2"
            entry = self.mapper.create_entry(title, text, html, slug, author_id)
            return entry
