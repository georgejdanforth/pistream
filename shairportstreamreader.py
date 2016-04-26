"""
Code in this module based on:
http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading
"""
import os
import time
from queue import Queue
from threading import Thread, Lock


class StreamReader(Thread):

    def __init__(self, stream, queue, lock):
        super().__init__(daemon=True)
        self.stream = stream
        self.queue = queue
        self.lock = lock

    def run(self):
        for line in iter(self.stream.readline, ''):
            with self.lock:
                self.queue.put(line)

    def eof(self):
        return not self.is_alive() and self.queue.empty()
