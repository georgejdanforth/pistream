import os
import time
from queue import Queue
from threading import Thread, Event

from fiforeader import FifoReader


class MetadataReader(FifoReader):

    def run(self):
        prev_metadata = None
        while not self.stopped():
            metadata = self.read_fifo()
            if (metadata != prev_metadata) and metadata is not None:
                prev_metadata = metadata
                print(metadata.strip())

            time.sleep(self.interval)
