from medoly.kanon import ui


@ui("user.html")
class UserView(object):

    __thing__ = """thing->User"""

    def render(self, uid):
        user = self.thing.find_by_uid(uid)
        return {"user": user}
