import math
import time
import threading
from collections import deque
import PySimpleGUI as sg


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

def mostrarresultado(angle,med):
    text=''
    if GlobalVars.measType==1:
        text=('Flexión dorsal '+str(GlobalVars.lr)+' '+str(round(angle))+' grados')
    elif GlobalVars.measType==0:
        text=('Flexión palmar: '+str(GlobalVars.lr)+' '+str(round(angle))+' grados')
    elif GlobalVars.measType==2:
        text=('Desviación cubital: '+str(GlobalVars.lr)+' '+str(round(angle))+' grados')
    elif GlobalVars.measType==3:
        text =('Desviación radial: '+str(GlobalVars.lr)+' '+str(round(angle))+' grados')
    elif GlobalVars.measType==4:
        text =('Pronosupinación: '+str(round(angle))+' grados')
    else:
        text=''
    layout=[[sg.Text(text)],
            [sg.Button('Si'), sg.Button('No')]]
    window = sg.Window('Guardar resultado?', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'No':
            sg.popup_ok('El resultado se ha descartado')
            break
        elif event == 'Si':
            sg.popup_ok('El resultado se ha guardado')
            break
    GlobalVars.ready = 0
    window.close()

class GlobalVars:
    isZero = 0
    ready = 0
    stopFlag = 0
    started = 0
    med = 0
    event = threading.Event()
    datomedio = 0
    stop_event=threading.Event()
    db = DataBuffer()  # aqui inicializamos como variable global el buffer de ángulos
    registered = False
    i=0
    measType=0
    lr=0
    uid = ''
    uid_session = ''
    nombre = 'unknown'
    palmar = 0
    dorsal = 0
    date = '12-12-2023'



def thread_function():
    t = 5
    while t:
        time.sleep(1)
        t -= 1
    if t == 0:
        print("Hilo finalizado!")
        GlobalVars.event.set()


def hiloconteo(secs):
    if(not GlobalVars.stop_event.is_set()):
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
            GlobalVars.i=0
            GlobalVars.db.clear()
            print("Buffer vacio, empezamos...")

    if(GlobalVars.i>100):
        print("Terminado...")
        GlobalVars.registered= True