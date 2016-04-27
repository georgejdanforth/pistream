import os
import time
from queue import Queue
from threading import Thread, Lock

from fiforeader import FifoReader


class MetadataReader(FifoReader):

    def run(self):
        prev_metadata = None
        while self.get_cmd() != 'terminate':
            metadata = self.read_fifo()
            if (metadata != prev_metadata) and metadata is not None:
                artist, track, album = self.parse_metadata(metadata)
                prev_metadata = metadata
                # print(artist + ', ' + track + ', ' + album)

            time.sleep(self.interval)
        os.close(self.fifo)

    def parse_metadata(self, metadata):
        info = []
        l, r = 0, 0
        for _ in range(3):
            l = metadata.find('=', r) + 1
            r = metadata.find('\n', l)
            info.append(metadata[l:r])
        return info
