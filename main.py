import os
import time
import subprocess
from queue import Queue
from threading import Thread, Lock

from fiforeader import FifoReader
from shairportstreamreader import StreamReader


fifoPath = "metadata/now_playing"


def main():

    startTime = time.time()

    fifoReaderLock = Lock()
    fifoReaderQueue = Queue()
    fifoReader = FifoReader(fifoPath, fifoReaderQueue, fifoReaderLock)

    shairport = subprocess.Popen(["./shairport -M ~/shairport1/metadata"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=True,
                                 universal_newlines=False)
    outLock = Lock()
    outQueue = Queue()
    outReader = StreamReader(shairport.stdout, outQueue, outLock)
    errLock = Lock()
    errQueue = Queue()
    errReader = StreamReader(shairport.stderr, errQueue, errLock)

    outReader.start()
    errReader.start()
    fifoReader.start()

    while time.time() - startTime < 45:
        while not outReader.eof() or not errReader.eof():
            while not outQueue.empty():
                with outLock:
                    line = outQueue.get()
                    print("stdout:", line)
            while not errQueue.empty():
                with errLock:
                    line = errQueue.get()
                    print("stderr:", line)
        time.sleep(0.1)

    with fifoReaderLock:
        fifoReaderQueue.put('terminate')

    while fifoReader.is_alive():
        pass
    fifoReader.join()

    shairport.terminate()

    while not outReader.eof() or not errReader.eof():
        pass
    outReader.join()
    errReader.join()

    shairport.stdout.close()
    shairport.stderr.close()


if __name__ == '__main__':
    main()
