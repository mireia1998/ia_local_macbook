import time
import threading


class GlobalVars:
    isZero = 0
    ready = 0
    stopFlag = 0
    started =0
    med=0
    event=threading.Event()




def thread_function():
    print("Thread starting...")
    t=5
    while t:
        time.sleep(1)
        t -= 1
        print("-1 sec")

    GlobalVars.event.set()


def on_thread_finish():
    print("Hilo finalizado")
    GlobalVars.event.set()
    if GlobalVars.med==0 :
        GlobalVars.isZero=1
    else:
        GlobalVars.ready=1



def hiloconteo(secs):

    mythread = threading.Thread(target=thread_function)
    mythread.start()




