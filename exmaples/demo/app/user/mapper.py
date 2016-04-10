from medoly.kanon import bloom

from .model import User


@bloom("mapper")
class UserMapper(object):

    def find_by_uid(self, uid):
        return User(uid, "Anna")
