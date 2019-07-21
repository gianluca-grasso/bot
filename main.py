from flask import Flask, Response, request

from lib import genio
from euro import euro

import json
import time
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import logging
import sys
import pickle
import requests
from difflib import SequenceMatcher


app = Flask(__name__)





def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


'''
def add(db, serie):

    
    for key in db:
        for ele in db[key]:
            if serie["bot_name"] != ele["bot_name"] and similar(serie["name"],ele["name"])>0.5:
                db[ele["name"]].append(serie)
                return
    
    db[serie["name"]] = [serie]
'''


def add(db, serie):


    res = []
    for ele in db:
        flag=True
        for x in ele["series"]:
            if serie["bot_name"]==x["bot_name"]:
                flag=False
                break
        if flag:
            res.append({"ref":ele, "ratio":similar(serie["name"],ele["name"])})

    if len(res)>0:
        x = sorted(res, key = lambda key: key["ratio"])[::-1][0]
        if x["ratio"]>0.6:
            x["ref"]["series"].append(serie)
            return
        

    db.append({"name":serie["name"], "series":[serie]})




@app.route("/download", methods=['POST'])
def download():
    r = requests.post("http://127.0.0.1:5001/download",data=request.data)
    return Response(status=r.status_code)


@app.route("/get_downloads")
def get_downloads():
    r = requests.get("http://127.0.0.1:5001/get_downloads")
    return Response(r.text, status = r.status_code, mimetype='application/json')





@app.route("/")
def main():
    return app.send_static_file("index.html")


@app.route("/find_episodes", methods=['POST'])
def find_episode():
    global bots

    link = json.loads(request.data)["link"]

    ret = []
    for bot in bots:
        bot_name = type(bot).__name__
        ret.append({"bot_name": bot_name, "results": bot.find_episodes(link)})

    print(ret)
    
    return Response(json.dumps(ret), mimetype='application/json')
    

@app.route("/find_serie/<string:name>")
def find_serie(name):
    global bots
    
    ret = []
    for bot in bots:
        bot_name = type(bot).__name__
        #ret.append({"bot_name":bot_name, "results":bot.find_serie(name)})

        series = bot.find_serie(name)
        for serie in series:
            serie["bot_name"]=bot_name
        
        for serie in series:
            add(ret,serie)

    
    #ret = bot.image_cache(ret)
    print(ret)

    return Response(json.dumps(ret), mimetype='application/json')





if __name__ == "__main__":
    global bots
    bots = [genio(), euro()]

    app.run()




