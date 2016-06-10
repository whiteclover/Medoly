#!/usr/bin/env python

from datetime import datetime
from medoly import kanon
from medoly.muses import Model

from blog.sqla import db


@kanon.bloom("mapper")
class EntryMapper(object):

    def __init__(self):
        self.model = Model("Entry")

    def find_by_id(self, entry_id):
        """Find entry by entry id"""
        return db.query(self.model).get(entry_id)

    def list_entries(self, limit=10, offset=0):
        """List entries page order by publish timestamp

        :param  int offset: the page number, defaults to 0
        :param int limit: the page size, defaults to 5

        :returns: list[Entry]
        """
        q = db.query(self.model).order_by(self.model.published.desc()).limit(limit)
        if offset:
            q.offset(offset)

        return q.all()

    def find_by_slug(self, slug):
        """Find entries by the entry slug

        :param string slug: the entry slug
        :returns: the entries
        :rtype: Entry
        """
        return db.query(self.model).filter(self.model.slug == slug).first()

    def create_entry(self, title, markdown, html, slug, author_id):
        """Create a enrty

        :param title: the nery title
        :type title: stirng
        :param markdown: the entry markdown cotent
        :type markdown: string
        :param html: the html content
        :type html: string
        :param slug: the slug
        :type slug: string
        :param author_id: the author id
        :returns: the entry

        """
        entry = self.model(title=title, markdown=markdown, html=html, slug=slug, author_id=author_id, published=datetime.now())
        db.add(entry)
        db.commit()
        return entry

    def save(self, entry):
        """Flush entry to database"""
        db.add(entry)
        db.commit()
        return entry
