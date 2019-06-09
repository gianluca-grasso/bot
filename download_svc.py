from flask import Flask, Response, request
from episodes import episodes, episode
from lib import genio
import json
import _thread
import time
app = Flask(__name__)


def download_th(num):
    global data

    while 1:
        time.sleep(1)

        x = data.get_episode_by_status(0)
        if x==None:
            continue

        #x.mock_start()
        bot = genio()
        x.start(bot)
        data.rem_episode(x)


@app.route("/download", methods=['POST'])
def download():
    global data

    t = json.loads(request.data)
    data.add_esisode_as_json_or_dict(t)
    
    return Response(status=200)

@app.route("/get_downloads")
def get_downloads():
    global data
    t = data.get_episodes_as_array_dict()
    return Response(json.dumps(t), mimetype='application/json')
        



if __name__ == "__main__":
    global data
    data = episodes()

    th = _thread.start_new_thread(download_th, (0,) )
    app.run(port=5001)