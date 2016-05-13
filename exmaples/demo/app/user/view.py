from medoly.kanon import menu


@menu("/user")
class UserPage(object):

    def get(self):
        uid = int(self.get_argument("uid"))
        self.render("user_index.html", uid=uid)


@menu("/user.json")
class UserJsonPage(object):

    __thing__ = """thing->User"""

    def get(self):
        uid = int(self.get_argument("uid"))
        user = self.thing.find_by_uid(uid)
        self.jsonify(user)
