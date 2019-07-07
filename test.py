from multiprocessing import Process, Value, Lock, Manager
from multiprocessing.managers import BaseManager
from multiprocessing import sharedctypes
import time
import numpy as np
import json
import os



path = "C:\\Users\\bingo\\Desktop\\sp\\17x10 Lo hobbit.mp4"
lm = os.path.getmtime(path)

print(lm)




import time

lm =          "Wed, 17 Apr 2019 15:14:01 GMT"
temp_time = time.strptime(lm, "%a, %d %b %Y %X %Z")
timestamp = time.mktime(temp_time)

print(timestamp)



