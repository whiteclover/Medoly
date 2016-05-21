#!/usr/bin/env python
#
# Copyright 2016 Medoly
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class SimplePlugin(object):

    """Plugin base class which auto-subscribes methods for known channels."""

    bus = None

    def __init__(self, bus):
        self.bus = bus

    def subscribe(self):
        """Register this object as a (multi-channel) listener on the bus."""
        for channel in self.bus.listeners:
            # Subscribe self.start, self.exit, etc. if present.
            method = getattr(self, channel, None)
            if method is not None:
                self.bus.subscribe(channel, method)

    def unsubscribe(self):
        """Unregister this object as a listener on the bus."""
        for channel in self.bus.listeners:
            # Unsubscribe self.start, self.exit, etc. if present.
            method = getattr(self, channel, None)
            if method is not None:
                self.bus.unsubscribe(channel, method)


class ThreadManager(SimplePlugin):

    """Manager for HTTP request threads.

    If you have control over thread creation and destruction, publish to
    the 'acquire_thread' and 'release_thread' channels (for each thread).
    This will register/unregister the current thread and publish to
    'start_thread' and 'stop_thread' listeners in the bus as needed.

    If threads are created and destroyed by code you do not control
    (e.g., Apache), then, at the beginning of every HTTP request,
    publish to 'acquire_thread' only. You should not publish to
    'release_thread' in this case, since you do not know whether
    the thread will be re-used or not. The bus will call
    'stop_thread' listeners for you when it stops.
    """

    threads = None
    """A map of {thread ident: index number} pairs."""

    def __init__(self, bus):
        self.threads = {}
        SimplePlugin.__init__(self, bus)
        self.bus.listeners.setdefault('acquire_thread', set())
        self.bus.listeners.setdefault('start_thread', set())
        self.bus.listeners.setdefault('release_thread', set())
        self.bus.listeners.setdefault('stop_thread', set())

    def acquire_thread(self):
        """Run 'start_thread' listeners for the current thread.

        If the current thread has already been seen, any 'start_thread'
        listeners will not be run again.
        """
        thread_ident = get_thread_ident()
        if thread_ident not in self.threads:
            # We can't just use get_ident as the thread ID
            # because some platforms reuse thread ID's.
            i = len(self.threads) + 1
            self.threads[thread_ident] = i
            self.bus.publish('start_thread', i)

    def release_thread(self):
        """Release the current thread and run 'stop_thread' listeners."""
        thread_ident = get_thread_ident()
        i = self.threads.pop(thread_ident, None)
        if i is not None:
            self.bus.publish('stop_thread', i)

    def stop(self):
        """Release all threads and run all 'stop_thread' listeners."""
        for thread_ident, i in self.threads.items():
            self.bus.publish('stop_thread', i)
        self.threads.clear()
    graceful = stop
