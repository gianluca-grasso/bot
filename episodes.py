from lib import genio
from parallel import Parallel_Downloader
import threading
import json
import time
import os










class episode:
    s = None
    e = None
    name = None
    link = None
    path = None
    src = None
    status = 0
    cpos = 0
    len = None
    Mb = 1024*1024
    percentage = 0


    def __init__(self, s, e, name, link, path):
        self.s = s
        self.e = e
        self.name = name
        self.link = link
        self.path = path+s+"x"+e+" "+self.path_for_windows(name)+".mp4"
        
        self.status = 0
        self.percentage = 0
        self.src = None
        self.len = 0


    def get_dict(self):
        return self.__dict__

    
    def path_for_windows(self, path):
        for ele in ["/",":","*","?","\"","<",">","|","\\"]:
            path = path.replace(ele,"")
        return path

    
    def get_id(self):
        return str(self.s)+str(self.e)+self.name


    def is_already_downloaded(self):
        if os.path.isfile(self.path) and os.path.getsize(self.path)==self.len:
            return True
        return False
    
    
    def preload(self, bot):
        
        self.src = bot.get_src_with_selenium_exp(self.link)
        self.len = bot.get_length(self.src)

        if self.is_already_downloaded():
            self.status = 3
        else:
            self.status = 1



    
    def watchdog(self, x):

        time.sleep(5)

        while self.status==2:

            self.percentage = x.get_percentage()
            print("th aggiorna: "+str(self.percentage))
            time.sleep(1)
        
        print("\n----------------------------------------\nDOWNLOAD FINITO\n----------------------------------------\n")
    
    '''
    0 = wait
    1 = src preloaded
    2 = downloading
    3 = done
    4 = error
    
    '''

    def start_fast(self, bot):

        if self.src==None:
            self.src = bot.get_src_with_selenium_exp(self.link)
            

        if self.src!=None:
            
            x = Parallel_Downloader(self.src, self.path)


            self.status = 2
            t = threading.Thread(target=self.watchdog, args=(x, ))
            t.daemon = True
            t.start()


            x.download(8)


            self.status = 3
            
            
            
        
        print("\nDOWNLOAD COMPLETATO\n")

        















class episodes:

    def __init__(self):
        self.episodes = {}

    def get_episodes(self):
        return self.episodes
    
    def add_esisodes_as_json_or_dict(self, x):

        if type(x).__name__ == "str":
            x = json.loads(x)
        

        for ele in x:
            epi = episode(**ele)
            id = epi.get_id()

            #aggiunge l'episodio solo se non già presente
            if not id in self.episodes:
                self.episodes[id] = epi

    
    def rem_episodes_by_id(self, ids):

        #molto permissiva
        if isinstance(ids, list):
            for id in ids:
                del self.episodes[id]
        else:
            del self.episodes[ids]

    

    def get_episode_by_status(self, status):
        for ele in self.episodes:

            t = self.episodes[ele]
            if t.status == status:
                return t

    def count_episodes_by_status(self, status):
        c = 0
        for ele in self.episodes:
            
            t = self.episodes[ele]
            if t.status == status:
                c+=1
        return c

    def get_episodes_as_array_dict(self):
        ret = []
        for ele in self.episodes:

            t = self.episodes[ele]
            ret.append(t.get_dict())
        return ret




