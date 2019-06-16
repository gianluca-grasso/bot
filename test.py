from multiprocessing import Process, Value, Lock, Manager
from multiprocessing.managers import BaseManager
from multiprocessing import sharedctypes
import time
import numpy as np
import json




class abc:
    
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def show(self):
        return str(self.a)+" - "+str(self.b)+" - "+str(self.c)

data = {}

def add(ele):
    id = str(ele.a)+str(ele.b)+str(ele.c)
    data[id] = ele



add(abc(0,0,0))
add(abc(1,0,0))
add(abc(0,1,0))
add(abc(1,1,0))

for ele in data:
    print(data[ele].show())








