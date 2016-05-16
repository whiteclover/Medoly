#!/usr/bin/env python
class AppContext(object):
    """The application context
    """

    def __init__(self):
        #: the requet handler hook entries
        self.hooks = []

        #: the reuqest handler classes
        self.routes = []

        #: the athem apllcation config settings
        self.settings = {}

        #: the error exception handler hook callbacks
        self.error_pages = {}

    def attach(self, point, callback, failsafe, priority, kwargs):
        self.hooks.append((point, callback, failsafe, priority, kwargs))

    def error_page(self, status_code, callback):
        self.error_pages[status_code] = callback

    def extend_routes(self, routes):
        self.routes.extend(routes)
