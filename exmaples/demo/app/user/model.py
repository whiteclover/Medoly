from medoly.kanon import bloom


@bloom("model")
class User(object):

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
