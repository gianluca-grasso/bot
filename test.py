from multiprocessing import Process, Value, Lock, Manager
from multiprocessing.managers import BaseManager
from multiprocessing import sharedctypes
import time
import numpy as np
import json
import os



a = [{"a":6},{"a":3},{"a":12},{"a":4},{"a":1},{"a":7},{"a":2}]

a = sorted(a, key = lambda key: key["a"])[::-1]

print(a)



