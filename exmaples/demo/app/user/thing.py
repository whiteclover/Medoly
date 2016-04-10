from medoly.kanon import bloom
from medoly.anthem import Backend


@bloom("thing")
class UserThing(object):

	def __init__(self):
		self.dao = Backend('User')

	def find_by_uid(self, uid):
		return self.dao.find_by_uid(uid)
