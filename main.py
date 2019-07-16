from flask import Flask, Response, request
from lib import genio
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

@app.route("/download", methods=['POST'])
def download():
    r = requests.post("http://127.0.0.1:5001/download",data=request.data)
    return Response(status=r.status_code)


@app.route("/get_downloads")
def get_downloads():
    r = requests.get("http://127.0.0.1:5001/get_downloads")
    return Response(r.text, mimetype='application/json')


@app.route("/")
def main():
    return app.send_static_file("index.html")


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




