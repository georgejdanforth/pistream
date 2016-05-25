import os
import time
import subprocess

from shairportstreamreader import StreamReader
from metadatareader import MetadataReader


subProcArgs = ["shairport -b 100 -M ~/pistream/metadata -l shairout -e shairout"]
metadataPath = "metadata/now_playing"


def refresh_state():
    for f in os.listdir("metadata"):
        os.remove("metadata/" + f)
    os.remove("shairout")
    os.mkfifo("shairout")


def main():

    refresh_state()

    shairport = subprocess.Popen(subProcArgs,
                                 stdout=None,
                                 stderr=None,
                                 shell=True,
                                 universal_newlines=True)

    threads = {"metadata":MetadataReader(metadataPath),
               "stream":StreamReader("shairout")}
    threads["stream"].start()

    while not "now_playing" in os.listdir("metadata"):
        time.sleep(1)

    threads["metadata"].start()

    startTime = time.time()

    while time.time() - startTime < 45: # time limit for testing
        art = [f for f in os.listdir("metadata") if f != "now_playing"]
        if len(art) != 0:
            for f in art:
                os.remove("metadata/" + f)
        time.sleep(0.1)

    shairport.terminate()

    for t in threads.values():
        t.stop()

    while any([threads[t].is_alive() for t in threads.keys()]):
        print([t for t in threads.keys() if threads[t].is_alive()])
        time.sleep(1)

    for t in threads.values():
        t.join()



if __name__ == '__main__':
    main()
