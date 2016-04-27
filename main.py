import os
import time
import subprocess
from queue import Queue
from threading import Thread, Lock

from metadatareader import MetadataReader
from shairportstreamreader import StreamReader


subProcArgs = ["shairport -M ~/pistream/metadata -l shairout -e shairout"]
metadataPath = "metadata/now_playing"


def main():

    startTime = time.time()

    metadataReaderLock = Lock()
    metadataReaderQueue = Queue()
    metadataReader = MetadataReader(metadataPath,
                                    metadataReaderQueue,
                                    metadataReaderLock)

    shairport = subprocess.Popen(subProcArgs,
                                 stdout=None,
                                 stderr=None,
                                 shell=True,
                                 universal_newlines=True)

    outReaderLock = Lock()
    outReaderQueue = Queue()
    outReader = StreamReader("shairout", outReaderQueue, outReaderLock)

    outReader.start()
    metadataReader.start()

    while time.time() - startTime < 45:
        time.sleep(0.1)

    with metadataReaderLock:
        metadataReaderQueue.put('terminate')
    with outReaderLock:
        outReaderQueue.put('terminate')

    while metadataReader.is_alive() or outReader.is_alive:
        pass
    metadataReader.join()
    outReader.join()

    shairport.terminate()


if __name__ == '__main__':
    main()
