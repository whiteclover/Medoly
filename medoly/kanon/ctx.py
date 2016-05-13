
class AppContext(object):

    def __init__(self):
        self.hooks = []
        self.routes = []
        self.error_pages = {}

    def attach(self, point, callback, failsafe, priority, kwargs):
        self.hooks.append((point, callback, failsafe, priority, kwargs))

    def error_page(self, status_code, callback):
        self.error_pages[status_code] = callback

    def extend_routes(self, routes):
        self.routes.extend(routes)
