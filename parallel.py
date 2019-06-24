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
        self.__downloaded = 0

        self.__blocks = []


    def __get_len(self, src):
        print(":::::::::::::::")
        r = requests.head(src, allow_redirects=True, verify=False)
        print("------------------")
        len = 0
        if (r.status_code==200):
            len = int(r.headers.get("Content-Length"))
        else:
            print("status_code: ",r.status_code)
        
        return len


    def __as_block(self, blockSize):

        blockNumber = round(self.__len/blockSize)
        blocks = []

        if blockNumber>1:

            for c in range(0,blockNumber-1):
                blocks.append({"src":self.__src, "start":blockSize*c, "end":blockSize*(c+1)-1, "lock":self.__lock, "fw":self.__fw, "state":0})
            blocks.append({"src":self.__src, "start":blockSize*(c+1), "end":self.__len, "lock":self.__lock, "fw":self.__fw, "state":0})

        else:

            blocks.append({"src":self.__src, "start":0, "end":self.__len, "lock":self.__lock, "fw":self.__fw, "state":0})

        return blocks


    def __block_download(self, block):
        
        src = block["src"]
        start = block["start"]
        end = block["end"]
        fw = block["fw"]
        lock = block["lock"]


        headers = {"Range":"bytes="+str(start)+"-"+str(end),"Connection":"close"}
        stream = requests.get(src, headers=headers, stream=True, allow_redirects=True, verify=False)


        status = stream.status_code
        print("STATUS: ",status)

        if status < 200 or status > 299:
            print("STATO DI ERRORE")
            #implementare


        count = 0
        block["state"] += 1


        try:

            for chunk in stream.iter_content(chunk_size=4096):
                if chunk:
                        
                    lock.acquire()

                    fw.seek(start+count)
                    fw.write(chunk)

                    x = len(chunk)
                    count += x
                    self.__downloaded += x

                    lock.release()
            
        except:

            #se vado in errore, ricreo un blocco di cio che non ho scaricato
            block["start"] += count
            self.__blocks.append(block)


        



    def download(self, nth):

        self.__blocks = self.__as_block(10)#20*Mb)
        while len(self.__blocks)>0:

            ava = nth - threading.active_count()+1

            for c in range(ava):
                block = self.__blocks.pop(0)
                t = threading.Thread(target=self.__block_download, args=(block, ))
                t.start()


    def get_len(self):
        return self.__downloaded



'''
x = Parallel_Downloader("http://127.0.0.1:8081/download","C:\\Users\\bingo\\Desktop\\b.txt")
print("download")
x.download(4)
'''