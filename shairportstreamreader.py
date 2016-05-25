import os
import time
from queue import Queue
from threading import Thread, Event

from fiforeader import FifoReader


class StreamReader(FifoReader):

    def run(self):
        prev_out = None
        while not self.stopped():
            out = self.read_fifo()
            if (out != prev_out) and (out is not None):
                prev_out = out
                print(out.strip())
            time.sleep(self.interval)
