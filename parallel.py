import time
import requests
import threading
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



Mb = 1024*1024


class Parallel_Downloader:

    def __init__(self, src, path):
        self.__src = src
        self.__path = path
        self.__fw = open(self.__path_for_windows(path),"wb")

        self.__headers = self.__get_headers()
        self.__len = int(self.__headers.get("Content-Length"))
        self.__lm = self.__lm_to_timestamp(self.__headers.get("Last-Modified"))
        self.__ETag = self.__headers.get("ETag")

        self.__lock = threading.Lock()
        self.__downloaded = 0

        self.__blocks = []

    def __lm_to_timestamp(self, lm):
        temp_time = time.strptime(lm, "%a, %d %b %Y %X %Z")
        return time.mktime(temp_time)

    def __path_for_windows(self, path):
        for ele in ["/",":","*","?","\"","<",">","|"]: #rimettere \\
            path = path.replace(ele,"")
        return path

    def __get_headers(self):
        r = requests.head(self.__src, allow_redirects=True, verify=False)
        
        if (r.status_code==200):
            return r.headers
        
        return {}


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


    def get_percentage(self):
        return round((self.__downloaded/self.__len)*100)


    def download(self, nth):

        
        if os.path.isfile(self.__path) and os.path.getsize(self.__path)==self.__len:
            print("IL FILE E' GIA' PRESENTE")
            return
        

        self.__blocks = self.__as_block(10*Mb)#20*Mb)
        try:

            while len(self.__blocks)>0 or threading.active_count()>2:

                time.sleep(1)
                ava = nth - threading.active_count()+3

                for c in range(ava):
                    print("\n\nAVVIO: "+str(c)+"\n\n")
                    block = self.__blocks.pop(0)
                    t = threading.Thread(target=self.__block_download, args=(block, ))
                    t.start()

        except:
            print("errore")


    def get_len(self):
        return self.__downloaded



'''
x = Parallel_Downloader("http://127.0.0.1:8081/download","C:\\Users\\bingo\\Desktop\\b.txt")
print("download")
x.download(4)
'''