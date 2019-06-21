import time
import requests
import threading


Mb = 1024*1024


class Parallel_Downloader:

    def __init__(self, src, path):
        self.__src = src
        self.__fw = open(path,"wb")
        self.__len = self.__get_len(src)
        self.__lock = threading.Lock()

    def __asBlock(self, blockSize):

        blockNumber = round(self.__len/blockSize)
        threads = []

        if blockNumber>1:

            for c in range(0,blockNumber-1):
                t = threading.Thread(target=self.__downloadBlock, args=(c, ))
                threads.append({"th":t, "src":self.__src, "start":blockSize*c, "end":blockSize*(c+1)-1, "lock":self.__lock, "fw":self.__fw, "state":0})

            t = threading.Thread(target=self.__download_block, args=(c+1, ))
            threads.append({"th":t, "src":self.__src, "start":blockSize*(c+1), "end":self.__len, "lock":self.__lock, "fw":self.__fw, "state":0})

        else:

            t = threading.Thread(target=self.__download_block, args=(0, ))
            threads.append({"th":t, "src":self.__src, "start":0, "end":self.__len, "lock":self.__lock, "fw":self.__fw, "state":0})


    def download(self, nth):

        blocks = self.__asBlock(20*Mb)
        ava = nth - threading.active_count()+1

        for c in range(ava):


        