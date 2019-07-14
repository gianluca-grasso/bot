import requests
import time
import dukpy
import bs4
import sys
import os
import pickle
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import json


class genio:

    __target = "https://ilgeniodellostreaming.se/"
    __session = None
    __episodes = None
    __num = 0
    __headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    __driver = None

    def skip_503(self, mode, link):

        if mode=="GET":
            req = self.__session.get(link, headers = self.__headers)
        elif mode=="HEAD":
            req = self.__session.head(link, headers = self.__headers, allow_redirects=True)
        elif mode=="POST":
            pass
        

        if req.status_code==503:
            html = req.text

            form = self.__get_form(html)
            res = self.__find_response(html)
            time.sleep(5)

            form["params"]["jschl_answer"] = res

            url0 = form["url"]
            params = form["params"]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',"Referer":link}
            req = self.__session.get(url0, headers=headers, params=params, allow_redirects=True)


        fw = open("session.pkl","wb")
        fw.write(pickle.dumps(self.__session))
        fw.close()


        return req

    def get_length(self, src):
        req = self.skip_503("HEAD", src)

        #if req.status_code != 200:
        #    return None

        #ritorna None se != 200 ?
        return int(req.headers.get("Content-Length"))

    def __sxe(self, link):
        t = re.search("(\d{1,3})[x|e](\d{1,3})", link, re.M|re.I)
        return {'s':int(t.group(1)),'e':int(t.group(2))}

    def valid_name(self, name):
        for ele in ["\\","/",":","*","?","\"","<",">","|"]:
            name = name.replace(ele,"")
        return name

    def __init__(self):

        self.__driver = webdriver.Firefox()
        self.__driver.install_addon(os.getcwd()+"\\ublock.xpi")

        if os.path.exists("session.pkl"):
            fr = open("session.pkl","rb")
            self.__session = pickle.load(fr)
            fr.close()
        else:
            self.__session = requests.Session()

    def __find_response(self, html):
        a = html.find("<script type=\"text/javascript\">")+31
        b = html.find("</script>",a)
        js = html[a:b]



        tmp = []
        tmp.append("var t = '"+self.__target[self.__target.find("//")+2:self.__target.rfind("/")]+"'")#integrare

        a = js.find("var s,t,o,p")+31
        b = js.find(";",a)

        x = js[a:b]
        var = x[:x.find("=")]

        tmp.append("var "+x)


        a = js.find(var,b)
        b = js.find("\n",a)

        x = js[a:b]

        for ele in x.split(";"):
            tmp.append(ele)

        c = tmp.pop()
        b = tmp.pop()
        a = tmp.pop()
        a += (";"+b+";"+c)


        x = a.find("=")
        a = "var a "+a[x:]

        tmp.append(a)
        tmp.append("a")

        r = dukpy.evaljs(tmp)
        return r

    def __get_form(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        form = {}

        for inp in soup.find_all("input"):
            #form.append({'name':inp.get("name"), 'value':inp.get("value")})
            #form.append({inp.get("name"):inp.get("value")})
            form.update({inp.get("name"):inp.get("value")})

        url = self.__target+soup.find("form").get("action")[1:]

        return {'url':url,'params':form}

    def find_serie(self, name):
        link = self.__target+"?s="+name

        req = self.skip_503("GET", link)
        soup = bs4.BeautifulSoup(req.text, 'html.parser')

        ret = []
        for item in soup.find_all("div",class_="result-item"):

            A = item.find_all("a")[1].text.lower()
            B = item.find("a").get("href")
            C = item.find("img").get("src")

            ret.append({'name':A, 'link':B, 'img':C})


        return ret

    def find_episodes(self, link):
        req = self.skip_503("GET", link)
        #req = self.__session.get(link, headers=self.__headers)
        html = req.text
        soup = bs4.BeautifulSoup(html, 'html.parser')

        print(req.status_code)

        ret = []

        for ele in soup.find_all("div",class_="episodiotitle"):
            link = ele.a.get("href")
            t = self.__sxe(link)

            s = t["s"]
            e = t["e"]
            name = ele.a.text

            ret.append({'s':s, 'e':e, 'name':name, 'link':link})

        return ret
        
    def get_cookie(self):
        return self.__session.cookies.get_dict()

    def image_cache(self, data):

        ret = []

        for ele in data:
            img = ele["img"]
            name = ele["name"]
            ext = img[img.rfind("."):]

            
            

            
            ele["img"] = "http://127.0.0.1:5000/static/tmp/"+name+ext
            path = "static\\tmp\\"+self.valid_name(name+ext)

            #se il file esiste non lo riscarico
            if os.path.isfile(path):
                ret.append(ele)
                continue

            req = self.__session.get(img, headers=self.__headers)

            if req.status_code == 200:

                fw = open(path, "wb")
                for chunk in req.iter_content(4096):
                    fw.write(chunk)
                fw.close()

                

                ret.append(ele)



        return ret

    def get_src_with_selenium(self, link):
        #driver = webdriver.Firefox()
        
        self.__driver.get(link)

        
        t = self.get_cookie()
        print(t)

        
        for name in t:
            value = t[name]
            #t = cookie.keys()
            #print(t)
            self.__driver.add_cookie({'name':name, 'value':value})
        

        #driver.get(link)


        element = WebDriverWait(self.__driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        
        src = element.get_attribute("src")
        self.__driver.switch_to_frame(element)


        if src.find("openload")>0:

            time.sleep(3)

            while 1:
                try:
                    self.__driver.execute_script("var divs = document.getElementsByTagName('div'); for (var c=0;c<divs.length;c++) if (divs[c].style.zIndex>100) divs[c].remove();")
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "videooverlay")))
                    element.click()
                    break
                except:
                    pass

            while 1:
                src = self.__driver.find_element_by_id("olvideo_html5_api").get_attribute("src")

                if src!="":
                    self.__driver.close()
                    return src

        else:

            '''
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            

            self.__driver.switch_to_frame(element)
            '''

            element = WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.ID, "videerlay")))

            while 1:
                element.click()
                src = self.__driver.find_element_by_id("dogevideo_html5_api").get_attribute("src")

                if src!="":
                    self.__driver.close()
                    return src

                time.sleep(1)
            
    def get_src_with_selenium_exp(self, link):
        #self.__driver = webdriver.Firefox()
        #self.__driver.install_addon(os.getcwd()+"\\ublock.xpi")
        self.__driver.get(link)


        element = WebDriverWait(self.__driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        
        src = element.get_attribute("src")
        self.__driver.switch_to_frame(element)

        element = WebDriverWait(self.__driver, 20).until(EC.element_to_be_clickable((By.ID, "videerlay")))
        time.sleep(1)
        element.click()


        while 1:
            
            src = self.__driver.find_element_by_id("dogevideo_html5_api").get_attribute("src")

            if src!="":
                #driver.close()
                return src

            time.sleep(1)


    def get_session(self):
        return self.__session
        

    



