class AppContext(object):

	def __init__(self):
		self.hooks = []
		self.routes = []


	def extend_routes(self, routes):
		self.routes.extend(routes)