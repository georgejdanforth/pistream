import os
import time
from queue import Queue
from threading import Thread, Lock

from fiforeader import FifoReader


class StreamReader(FifoReader):

    def __init__(self, fifoPath, queue, lock, interval=0.1):
        super().__init__(fifoPath, queue, lock, interval)
        self.listening = False
        self.streaming = False

    def run(self):
        prev_out = None
        while self.get_cmd() != 'terminate':
            out = self.read_fifo()
            if (out != prev_out) and (out is not None):
                print(out)
            time.sleep(self.interval)
        os.close(self.fifo)
