from multiprocessing import Process, Value, Lock, Manager
from multiprocessing.managers import BaseManager
from multiprocessing import sharedctypes
import time
import numpy as np
import json




def test(x):
    if isinstance(x, list):
        print(x,"array")
    else:
        print(x,"scalare")


test(4)
test([4,5,3])
test([4,53,34,6])
test(45)






