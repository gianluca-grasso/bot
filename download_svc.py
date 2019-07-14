from flask import Flask, Response, request
from episodes import episodes, episode
from lib import genio
import json
import _thread
import time
import socket
app = Flask(__name__)






def preload_src():
    global data
    global bot
    while 1:
        time.sleep(5)

        if data.count_episodes_by_status(1) < 2:
            x = data.get_episode_by_status(0)
            if x!=None:

                x.preload(bot)
                if x.status==3:
                    data.rem_episodes_by_id(x.get_id())



def flask_th():
    app.run(port=5001)


@app.route("/download", methods=['POST'])
def download():
    global data

    t = json.loads(request.data)
    data.add_esisodes_as_json_or_dict(t)
    
    return Response(status=200)

@app.route("/get_downloads")
def get_downloads():
    global data
    t = data.get_episodes_as_array_dict()
    return Response(json.dumps(t), mimetype='application/json')
        
'''
@app.route("/rem_downloads_by_id/<id>", methods=['GET'])
def rem_downloads(id):
    global data

    data.rem_episodes_by_id(id)

    return Response(status=200)
'''

if __name__ == "__main__":
    global data
    global bot
    data = episodes()
    bot = genio()



    th0 = _thread.start_new_thread(flask_th, ())
    th1 = _thread.start_new_thread(preload_src, ())

    while 1:
        time.sleep(1)
        
        x = data.get_episode_by_status(1)
        if x != None:
            
            
            x.start_fast(bot)
            print("rimuovo episodio")
            data.rem_episodes_by_id(x.get_id())
            #print("download:",x.get_id())


