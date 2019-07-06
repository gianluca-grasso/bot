from flask import Flask, Response, request
from episodes import episodes, episode
from lib import genio
import json
import _thread
import time
import socket
app = Flask(__name__)









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
        

@app.route("/rem_downloads_by_id/<id>", methods=['GET'])
def rem_downloads(id):
    global data

    data.rem_episodes_by_id(id)

    return Response(status=200)

'''
@app.route("/rem_downloads_by_id", methods=['POST'])
def rem_downloads():
    global data

    t = json.loads(request.data)["ids"]
    data.rem_episodes_by_id(t)

    return Response(status=200)
'''

if __name__ == "__main__":
    global data
    data = episodes()



    th0 = _thread.start_new_thread(flask_th, ())

    while 1:
        time.sleep(5)

        x = data.get_episode_by_status(0)
        if x != None:
            
            bot = genio()
            x.start_fast(bot)
            data.rem_episodes_by_id(x.get_id())
            #print("download:",x.get_id())