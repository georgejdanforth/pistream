import os
import time
from queue import Queue
from threading import Thread, Lock


class FifoReader(Thread):

    def __init__(self, fifoPath, queue, lock, interval=0.1):
        super().__init__(daemon=True)
        self.fifo = os.open(fifoPath, os.O_RDONLY | os.O_NONBLOCK)
        self.queue = queue
        self.lock = lock
        self.interval = interval

    def get_cmd(self):
        with self.lock:
            if not self.queue.empty():
                return self.queue.get()
            else:
                return None

    def read_fifo(self):
        try:
            data_bytes = os.read(self.fifo, 2048)
            data = data_bytes.decode('utf-8')
        except BlockingIOError:
            return None

        if data == '':
            return None
        else:
            return data
