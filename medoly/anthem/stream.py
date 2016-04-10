import json
import httplib
import tornado.web
import tornado.ioloop
import logging 


LOG = logging.getLogger(__name__)

class Event():
    """
    Class that defines an event, its behaviour and the matching actions
    LISTEN is the GET event that will open an event source communication
    FINISH is the POST event that will end an event source communication started by LISTEN
    ACTIONS contains the list of acceptable POST targets.
    target is the token that matches an event source channel
    action contains the name of the action (which shall be in ACTIONS)
    value contains a list of every lines of the value to be parsed
    """
    content_type = "text/plain"

    LISTEN = "poll"
    FINISH = "close"
    ACTIONS=[FINISH]

    """Property to split multiline values"""
    @classmethod
    def get_value(self):
        pass

    @classmethod
    def set_value(self, v):
        pass

    value = property(get_value,set_value)

    def __init__(self, target, action, value=None):
        """
        Creates a new Event object with
        @param target a string matching an open channel
        @param action a string matching an action in the ACTIONS list
        @param value a value to be embedded
        """
        self.target = target
        self.action = action
        self.set_value(value)

##

class StringEvent(Event):
    ACTIONS=["ping",Event.FINISH]

    """Property to enable multiline output of the value"""
    def get_value(self):
        return [line for line in self._value.split('\n')]

    def set_value(self, v):
        self._value = v

    value = property(get_value,set_value)

class JSONEvent(Event):
    content_type = "application/json"

    LISTEN = "poll"
    FINISH = "close"
    ACTIONS=["ping",FINISH]

    """Property to enable JSON checking of the value"""
    def get_value(self):
        return [json.dumps(self._value)]

    def set_value(self, v):
        self._value = json.loads(v)

    value = property(get_value,set_value)


class EventSourceHandler(tornado.web.RequestHandler):
    _connected = {}
    _events = {}

    def initialize(self, event_class=StringEvent):
        """
        Takes an Event based class to define the event's handling
        """
        self._event_class = event_class

    """Tools"""

    def push(self, event):
        """
        For a given event, write event-source outputs on current handler
        @param event Event based incoming event
        """
        self.write("event: "+unicode(event.action)+"\r\n")
        for line in event.value:
            self.write("data: %s\r\n" % (unicode(line),))
        self.write("\r\n")
        self.flush()

    def buffer_event(self, target, action, value=None):
        """
        creates and store an event for the target
        @param target string identifying current target
        @param action string matching one of Event.ACTIONS
        @param value string containing a value
        """
        self._events[target].append(self._event_class(target, action, value))

    def is_connected(self, target):
        """
        @param target string identifying a given target
        @return true if target is connected
        """
        return target in self._connected.values()

    def set_connected(self, target):
        """
        registers target as being connected
        @param target string identifying a given target
        this method will add target to the connected list, 
        and create an empty event buffer
        """
        LOG.debug("set_connected(%s)" % (target,))
        self._connected[self] = target
        self._events[target] = []

    def set_disconnected(self):
        """
        unregisters current handler as being connected
        this method will remove target from the connected list,
        and delete the event buffer
        """
        try:
            target = self._connected[self]
            LOG.debug("set_disconnected(%s)" % (target,))
            del(self._events[target])
            del(self._connected[self])
        except Exception, err:
            LOG.error("set_disconnected(%s,%s): %s", str(self), target, err)

    def write_error(self, status_code, **kwargs):
        """
        overloads the write_error() method of RequestHandler, to
        support more explicit messages than only the ones from httplib.
        """
        if self.settings.get("debug") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            if 'mesg' in kwargs:
                self.finish("<html><title>%(code)d: %(message)s</title>" 
                            "<body>%(code)d: %(mesg)s</body></html>\n" % {
                        "code": status_code,
                        "message": httplib.responses[status_code],
                        "mesg": kwargs["mesg"],
                        })
            else:
                self.finish("<html><title>%(code)d: %(message)s</title>" 
                            "<body>%(code)d: %(message)s</body></html>\n" % {
                        "code": status_code,
                        "message": httplib.responses[status_code],
                        })

    """Synchronous actions"""

    def post(self,action,target):
        """
        Triggers an event
        @param action string defining the type of event
        @param target string defining the target handler to send it to
        this method will look for the request body to get post's data.
        """
        LOG.debug("post(%s,%s)" % (target,action))
        self.set_header("Accept", self._event_class.content_type)
        if target not in self._connected.values():
            self.send_error(404,mesg="Target is not connected")
        elif action not in self._event_class.ACTIONS:
            self.send_error(404,mesg="Unknown action requested")
        else:
            try:
                self.buffer_event(target,action,self.request.body)
            except ValueError, ve:
                self.send_error(400,mesg="JSON data is not properly formatted: <br />%s" % (ve,))

    """Asynchronous actions"""
    
    def _event_generator(self,target):
        """
        parses all events buffered for target and yield them
        """
        for ev in self._events[target]:
            self._events[target].remove(ev)
            yield ev
        
    def _event_loop(self):
        """
        for target matching current handler, gets and forwards all events
        until Event.FINISH is reached, and then closes the channel.
        """
        if self.is_connected(self.target):
            for event in self._event_generator(self.target):
                if event.action == self._event_class.FINISH:
                    self.set_disconnected()
                    self.finish()
                    return
                self.push(event)
            tornado.ioloop.IOLoop.instance().add_callback(self._event_loop)

    @tornado.web.asynchronous
    def get(self,action,target):
        """
        Opens a new event_source connection and wait for events to come
        Returns error 423 if the target token already exists
        Redirects to / if action is not matching Event.LISTEN.
        """
        LOG.debug("get(%s,%s)" % (target, action))
        if action == self._event_class.LISTEN:
            self.set_header("Content-Type", "text/event-stream")
            self.target = target
            if self.is_connected(target):
                self.send_error(423,mesg="Target is already connected")
                return
            self.set_connected(target)
            tornado.ioloop.IOLoop.instance().add_callback(self._event_loop)
        else:
            self.redirect("/",permanent=True)
        
    def on_connection_close(self):
        """
        overloads RequestHandler's on_connection_close to disconnect
        currents handler on client's socket disconnection.
        """
        LOG.debug("on_connection_close()")
        self.set_disconnected()
