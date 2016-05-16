class Pros(object):

    @staticmethod
    def create(event_name, callbacks, *args, **kw):
        return Pros(event_name, callbacks, args, kw)

    def __json__(self):
        return {
            'name': self.event_name,
            'args': self.args,
            'kw': self.kw
        }

    def run(self):
        for callback in self.callbacks:
            callback(*self.args, **self.kw)

    def __init__(self, event_name, callbacks, args, kw):
        self.callbacks = callbacks
        self.event_name = event_name
        self.args = args
        self.kw = kw
