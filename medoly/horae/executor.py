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


import logging
import time
import threading
import sys
import Queue
from datetime import datetime, timedelta

try:
    from thread import get_ident
except ImportError:
    from _thread import get_ident


from .pros import Pros

LOGGER = logging.getLogger(__name__)

_SHUTDOWNTASK = object()


class ThreadPoolExecutor(object):

    # the total time for worker thread to cleanly exit
    SHOTDOWN_TIMEOUT = 5

    def __init__(self, bus, queue, minthreads=5, maxthreads=10):
        """[summary]

        [description]
        :param bus: [description]
        :type bus: [type]
        :param queue: [description]
        :type queue: [type]
        :param minthreads: [description], defaults to 5
        :type minthreads: number, optional
        :param maxthreads: [description], defaults to 10
        :type maxthreads: number, optional
        :raises: TypeError
        """

        minthreads = minthreads or 1
        minthreads = 1 if minthreads <= 0 else minthreads
        maxthreads = maxthreads or 10
        maxthreads = 50 if maxthreads > 50 else maxthreads
        if maxthreads <= minthreads:
            raise TypeError(
                'maxthreads:%d must be greater than minthreads:%d', maxthreads, minthreads)

        self.bus = bus
        self.ready = False
        self._append_tasks = queue or Queue.Queue()
        self._idel_tasks = Queue.Queue()
        self.threadpool = ThreadPool(self, minthreads, maxthreads)
        self.heartbeat = HeartBeat(self._periodic_action, 5)
        self.clear_time = time.time()

    def _periodic_action(self):

        if (time.time() - self.clear_time) > 300:
            self.clear_time = time.time()

        # clear idle tasks
        idel_queue_size = self._idel_tasks.qsize()
        for _ in range(idel_queue_size):
            task = self.get()
            self.execute(task, True)

    get = lambda self: self._idel_tasks.get()

    put = lambda self, task: self._idel_tasks.put(task)

    def run(self):
        LOGGER.debug('Starting executor ....')
        LOGGER.debug('Master thread : %d', get_ident())
        self.ready = True
        self.threadpool.start()
        self.heartbeat.start()

        while self.ready:
            try:
                tasks = self.claim()
                if not tasks:
                    LOGGER.debug('No task sleep 5 secs')
                    time.sleep(5)
                    continue

                for task in tasks:
                    LOGGER.debug('current_task: %s', task)
                    self.execute(task)

            except Exception as e:
                cls, e, tb = sys.exc_info()
                LOGGER.exception('Unhandled Error %s', e)

        LOGGER.debug('Stoping executor...')
        self.stop()

    def stop(self):
        self.heartbeat.stop()
        self.threadpool.stop(self.SHOTDOWN_TIMEOUT)

    def execute(self, task, retry=False):
        try:
            done = False
            thread = self.threadpool.pop()
            if thread:
                LOGGER.debug('Execute in thread: %s', thread)
                thread.current_task = task
                thread.resume()
                done = True
            elif not retry:
                LOGGER.info(
                    'Thread Pool is Full, put the the task:%s to idel_queue', task.name)
                self.put(task)
                time.sleep(1)
            else:
                LOGGER.info("Faield task:%s, retry...", task.name)

        except (KeyboardInterrupt, SystemExit):
            self.ready = False
            if not done and thread:
                thread.current_task = _SHUTDOWNTASK
                thread.resume()
        except Exception as e:
            LOGGER.error('Execute error : %s', e)
            LOGGER.info("Faield task:%s, retry...", task.name)

    def put(sef, pros):
        self._append_tasks.put(pros)

    def claim(self):
        return self._append_tasks.get()


class HeartBeat(threading.Thread):

    def __init__(self, callback, interval=5):
        self.callback = callback
        self.interval = interval
        self.ready = False
        threading.Thread.__init__(self)

    def run(self):
        self.ready = True
        while self.ready:
            time.sleep(self.interval)
            self.callback()

    def stop(self):
        self.ready = False
        if self.isAlive():
            self.join()


class ThreadPool(object):

    def __init__(self, executor, min, max):
        self.executor = executor
        self.min = min
        self.max = max
        self._created = 0
        self._lock = threading.Lock()
        self._in_use_threads = {}
        self._idel_threads = []

    def start(self):
        for i in range(self.min):
            with self._lock:
                self._created += 1
                thread = self._new_thread()
                self._idel_threads.append(thread)

    def push(self, thread):
        with self._lock:
            if thread in self._in_use_threads:
                del self._in_use_threads[thread]
            self._idel_threads.append(thread)

    def pop(self):
        """Non-block pop an idle thread, if not get returns None"""
        thread = None
        self._lock.acquire()
        if self._idel_threads:
            thread = self._idel_threads.pop(0)
            self._in_use_threads[thread] = True
        elif self._created < self.max:
            self._created += 1
            thread = self._new_thread()
            self._in_use_threads[thread] = True
        self._lock.release()
        return thread

    def _new_thread(self):
        return WorkerThread(self.executor, self)

    def stop(self, timeout=5):
        # Must shut down threads here so the code that calls
        # this method can know when all threads are stopped.

        while True:
            time.sleep(1)
            with self._lock:
                if self._in_use_threads or self._idel_threads:
                    while self._idel_threads:
                        worker = self._idel_threads.pop(0)
                        worker.resume()
                        # worker.event.clear()
                else:
                    break


class WorkerThread(threading.Thread):

    def __init__(self, executor, pool):
        self.ready = False
        self.event = threading.Event()
        self.executor = executor
        self.current_task = None
        self.pool = pool
        threading.Thread.__init__(self)
        self.start()

    def suspend(self):
        self.event.clear()
        self.event.wait()

    def resume(self):
        self.event.set()

    def run(self):
        self.ready = True
        LOGGER.debug('Starting thread %d', get_ident())
        while self.ready:
            self.suspend()
            if self.current_task == _SHUTDOWNTASK:
                # shutdown the worker thread
                self.ready = False
                break
            try:
                if self.current_task:
                    self.current_task.run()
            except Exception as e:
                cls, e, tb = sys.exc_info()
                LOGGER.exception(
                    'Unhandled Error in thread:%s %s', get_ident(), e)
            finally:
                self.current_task = None
                self.pool.push(self)
        self.event.clear()
