from flask import Flask, Response, request, render_template
from lib import genio
from config import config
import json
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import logging
import sys
import pickle
import requests


app = Flask(__name__)






'''
@app.route("/download", methods=['POST'])
def download():
    global data

    t = json.loads(request.data)
    data.add_esisodes_as_json_or_dict(t)
    
    return Response(status=200)
'''

'''
@app.route("/download", methods=['POST'])
def download():
    r = requests.post("http://127.0.0.1:5001/download",data=request.data)
    return Response(status=r.status_code)


@app.route("/get_downloads")
def get_downloads():
    r = requests.get("http://127.0.0.1:5001/get_downloads")
    return Response(r.text, mimetype='application/json')
'''


@app.route("/")
def main():


    #config("main.pkl").set_config("last_path","\\\\a\\\\b\\\\".encode("utf8")).save_config("main.pkl")

    path = None
    #path = config("main.pkl").get_config("last_path").decode("cp1251")
    if path==None:
        path = "riempi"


    return render_template('index.html', last_path=path)
    #return app.send_static_file("index.html")


'''
@app.route("/save_last_path", methods=['POST'])
def save_last_path():
    global configs
    configs["last_path"] = request.data

    fw = open("frontend_config.pkl","wb")
    fw.write(pickle.dumps(configs))
    fw.close()
'''


@app.route("/find_episodes", methods=['POST'])
def find_episode():
    global bot

    link = json.loads(request.data)["link"]
    ret = bot.find_episodes(link)
    
    return Response(json.dumps(ret), mimetype='application/json')
    

@app.route("/find_serie/<string:name>")
def find_serie(name):
    global bot
    
    ret = bot.find_serie(name)
    ret = bot.image_cache(ret)

    return Response(json.dumps(ret), mimetype='application/json')





if __name__ == "__main__":
    global bot
    bot = genio()

    app.run()




