#!/usr/bin/env python

from blog.security import session

from medoly import kanon


@kanon.hook("on_start_request")
def on_start_request(req_handler):
    """on start request hook"""
    session.load(req_handler)


@kanon.error_page(404)
def not_found(req_handler, code, **kw):
    """Not Found Page"""
    req_handler.render("404.html", page_title='Page Not Found')
