import os
import time
from queue import Queue
from threading import Thread, Event


class FifoReader(Thread):

    def __init__(self, fifoPath, interval=0.1):
        super().__init__(daemon=True)
        self.fifoPath = fifoPath
        self.interval = interval
        self._stop_ = Event()

    def stop(self):
        self._stop_.set()

    def stopped(self):
        return self._stop_.isSet()

    def read_fifo(self):
        if self.stopped():
            return None

        fifo = os.open(self.fifoPath, os.O_RDONLY, os.O_NONBLOCK)
        try:
            data_bytes = os.read(fifo, 2048)
        except BlockingIOError:
            os.close(fifo)
            return None

        os.close(fifo)

        data = data_bytes.decode('utf-8')
        if data == '':
            return None
        else:
            return data
