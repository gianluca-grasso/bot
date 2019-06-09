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




