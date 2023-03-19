import math
import time
import threading
from collections import deque


class DataBuffer:
    def __init__(self):
        self.buffer = []
        self.total = 0
        self.avg = 0

    def insert(self, data):
        self.buffer.append(data)
        self.total += data
        n = len(self.buffer)
        self.avg = self.total / n
        if n > 1:
            var = sum((x - self.avg) ** 2 for x in self.buffer) / (n - 1)
            std = var ** 0.5
            if std > 0:
                k = 2  # constant factor to control buffer size
                size = int(k * var / std ** 2)
                size = max(size, 2)
                self.buffer = self.buffer[-size:]
                self.total = sum(self.buffer)
                self.avg = self.total / len(self.buffer)

    def clear(self):
        self.buffer.clear()
        self.total = 0
        self.avg = 0


class GlobalVars:
    isZero = 0
    ready = 0
    stopFlag = 0
    started = 0
    med = 0
    event = threading.Event()
    datomedio = 0
    db = DataBuffer()  # aqui inicializamos como variable global el buffer de ángulos
    registered = False
    i=0


def thread_function():
    print("Hilo comenzando...")
    t = 5
    while t and GlobalVars.stopFlag == 0:
        time.sleep(1)
        t -= 1
        print("-1 sec, " + str(t))
    if t == 0:
        print("Hilo finalizado!")
        GlobalVars.event.set()


def hiloconteo(secs):
    mythread = threading.Thread(target=thread_function)
    mythread.start()


def processnumber(angle):
    if (GlobalVars.datomedio == 0):
        GlobalVars.db.insert(angle)
        GlobalVars.datomedio = GlobalVars.db.avg
    else:
        if abs(angle - GlobalVars.datomedio) < 3:
            GlobalVars.db.insert(angle)
            GlobalVars.datomedio = GlobalVars.db.avg
            print(str(GlobalVars.datomedio))
            GlobalVars.i=GlobalVars.i+1
            print(str(GlobalVars.i))
        else:
            GlobalVars.datomedio = 0
            GlobalVars.db.clear()
            print("Buffer vacio, empezamos...")

    if(GlobalVars.i>100):
        print("Terminado...")
        GlobalVars.registered= True
