import os
import time
from queue import Queue
from threading import Thread, Lock


class FifoReader(Thread):

    def __init__(self, fifoPath, queue, lock, interval=0.25):
        super().__init__(daemon=True)
        self.fifo = os.open(fifoPath, os.O_RDONLY | os.O_NONBLOCK)
        self.queue = queue
        self.lock = lock
        self.interval = interval

    def run(self):
        prev_metadata = None
        print("fifoReader started")

        while True:

            with self.lock:
                if not self.queue.empty():
                    cmd = self.queue.get()
                    # TODO: add options for cmd received from main thread
                    if cmd == 'terminate':
                        break

            metadata = self.read_fifo()
            if (metadata != prev_metadata) and metadata is not None:
                artist, track, album = self.parse_metadata(metadata)
                prev_metadata = metadata
                # print(artist + ', ' + track + ', ' + album)

            time.sleep(self.interval)
        os.close(self.fifo)

    def read_fifo(self):
        try:
            metadata_bytes = os.read(self.fifo, 2048)
            metadata = metadata_bytes.decode('utf-8')
        except BlockingIOError:
            return None

        if metadata == '':
            return None
        else:
            return metadata

    def parse_metadata(self, metadata):
        info = []
        l, r = 0, 0
        for _ in range(3):
            l = metadata.find('=', r) + 1
            r = metadata.find('\n', l)
            info.append(metadata[l:r])
        return info
