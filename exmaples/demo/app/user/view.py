from medoly.kanon import menu

@menu("/user")
class Index(object):

	def get(self):
		uid = int(self.get_argument("uid"))
		self.render("user_index.html", uid=uid)
