import time
import requests
import threading
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



Mb = 1024*1024


class Parallel_Downloader:

    
    

    def __init__(self, src, path):
        self.src = src
        self.path = path
        self.fw = open(path,"wb")

        self.headers = self.__get_headers()
        self.len = int(self.headers.get("Content-Length"))
        self.ETag = self.headers.get("ETag")

        self.lock = threading.Lock()
        self.downloaded = 0

        self.blocks = []

        self.active_th = 0
        self.speed = 0
        self.saved_len = 0

    def __lm_to_timestamp(self, lm):
        temp_time = time.strptime(lm, "%a, %d %b %Y %X %Z")
        return time.mktime(temp_time)

    def __get_headers(self):
        r = requests.head(self.src, allow_redirects=True, verify=False)
        
        if (r.status_code==200):
            return r.headers
        
        return {}


    def __as_block(self, blockSize):

        blockNumber = round(self.len/blockSize)
        blocks = []

        if blockNumber>1:

            for c in range(0,blockNumber-1):
                blocks.append({"src":self.src, "start":blockSize*c, "end":blockSize*(c+1)-1, "lock":self.lock, "fw":self.fw, "state":0})
            blocks.append({"src":self.src, "start":blockSize*(c+1), "end":self.len, "lock":self.lock, "fw":self.fw, "state":0})

        else:

            blocks.append({"src":self.src, "start":0, "end":self.len, "lock":self.lock, "fw":self.fw, "state":0})

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
                    self.downloaded += x

                    lock.release()
            
        except:

            #se vado in errore, ricreo un blocco di cio che non ho scaricato
            block["start"] += count
            self.blocks.append(block)

        
        
        lock.acquire()
        self.active_th-=1
        lock.release()




    def get_percentage(self):
        return round((self.downloaded/self.len)*100)


    def download(self, nth):

        
        print("start download")
        self.blocks = self.__as_block(20*Mb)

        try:
            while self.len != self.downloaded or self.active_th>0:
                time.sleep(1)

                ava = min(nth-self.active_th, len(self.blocks))
                print("Thread count: "+str(self.active_th))

                for c in range(ava):
                    print("new Thread started")
                    block = self.blocks.pop(0)
                    t = threading.Thread(target=self.__block_download, args=(block, ))
                    t.daemon = True

                    self.lock.acquire()
                    self.active_th += 1
                    self.lock.release()

                    t.start()

                self.speed = float(self.downloaded - self.saved_len)/1048576.0
                self.saved_len = self.downloaded


        except Exception as e:
            print(e)






'''
x = Parallel_Downloader("http://127.0.0.1:8081/download","C:\\Users\\bingo\\Desktop\\b.txt")
print("download")
x.download(4)
'''