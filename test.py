from multiprocessing import Process, Value, Lock, Manager
import time
import numpy as np




db = [{"a":"0","b":1,"c":2},{"d":"0","e":1,"f":2}]
res = []

for ele in db:
    print(ele)
    


    t = ele.keys()
    res.append({"name":t[0], "value":t[1]})
    
    


'''
def process(data):
    while 1:
        time.sleep(1)

        t = data["list"]
        n = t.pop(0)
        data["list"] = t
        #n = data["list"].pop(0)

        print(n)



if __name__ == "__main__":

    
    manager = Manager()
    
    data = manager.dict()
    data["command"] = "download"
    data["list"] = [{'id':0, 'value':2}, {'id':1, 'value':5}, {'id':2, 'value':7}]
    

    p = Process(target=process, args=(data, ))
    p.start()

    while 1:
        time.sleep(1)
        print(data)
    

'''