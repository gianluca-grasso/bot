from multiprocessing import Process, Value, Lock, Manager
from multiprocessing.managers import BaseManager
from multiprocessing import sharedctypes
import time
import numpy as np
import json


def test(data):
    pass


if __name__ == "__main__":

    pro = multiprocessing.Process(target=test, args=(data,))
    pro.start() 


