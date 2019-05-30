from flask import Flask, Response, request
from lib import genio
import json
import time
from multiprocessing import Process, Manager
import logging
import sys
app = Flask(__name__)


#useless legacy
download_path = "C:\\Users\\bingo\\Desktop\\lw\\"




def process_download(data):

    bot = genio()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}

    while 1:
        time.sleep(1)

        #continue
        
        cmd = data["cmd"]
        t = data["list"]


        if len(t)>0:
            ele = t[0]
            #ele = t.pop(0)
            path = ele["path"]+str(ele["s"])+"x"+str(ele["e"])+" - "+ele["name"]+".mp4"
            link = ele["link"]

            src = bot.get_src_with_selenium(link)
            #src = bot.get_src_from_link_with_selenium(link)
            print("src =",src)
            req = bot.get_session().get(src, headers=headers, stream=True)

            

            size = bot.get_length(src)
            if size==None:
                print("Error: length undefined")
                time.sleep(5)
                continue


            count = 0
            print("size = "+str(size))



            if req.status_code==200:
                fw = open(path, "wb")
                for chunk in req.iter_content(4096):
                    count += len(chunk)
                    fw.write(chunk)

                    p = int((float(count)/float(size))*100.0)

                    if ele["status"] != p:
                        print(">",p)
                        ele["status"] = p
                        t[0] = ele
                        data["list"] = t

                fw.close()

            t.pop(0)
            data["list"] = t
            
        












@app.route("/")
def main():
    return app.send_static_file("index.html")


@app.route("/get_downloads")
def get_downloads():
    global data
    return Response(json.dumps(data["list"]), mimetype='application/json')



@app.route("/get_cookie")
def get_cookie():
    bot = genio()
    cookie = eval(bot.get_cookie())

    return Response(json.dumps(cookie), mimetype='application/json')


@app.route("/find_episodes", methods=['POST'])
def find_episode():

    link = json.loads(request.data)["link"]

    bot = genio()
    ret = bot.find_episodes(link)
    return Response(json.dumps(ret), mimetype='application/json')
    

@app.route("/find_serie/<string:name>")
def find_serie(name):
    
    bot = genio()
    data = bot.find_serie(name)

    data = bot.image_cache(data)

    return Response(json.dumps(data), mimetype='application/json')


@app.route("/download", methods=['POST'])
def download():
    global data
    
    inputs = json.loads(request.data)

    t = data["list"]
    for ele in inputs:
        t.append(ele)

    data["list"] = t

    
    
    ret = {"status":"OK"}
    return Response(json.dumps(ret), mimetype='application/json')


if __name__ == "__main__":
    
    global data
    
    data = Manager().dict()
    data["cmd"] = ""
    data["list"] = []
    
    p = Process(target=process_download, args=(data, ))
    p.start()

    app.run()



'''
link = "https://ilgeniodellostreaming.pw/episodi/lethal-weapon-2x1/"

bot = genio()
bot.download_from_openload_embedded_player_link(link, "C:\\Users\\bingo\\Desktop\\bot\\download\\a.mp4")
'''

