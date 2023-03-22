
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
    datomedio = 0
    db = DataBuffer()  # aqui inicializamos como variable global el buffer de ángulos
    registered = False
    i=0
    measType=0
    lr=0
    uid=''
    uid_session=''
    nombre='unknown'
    palmar=0
    dorsal=0
    date='12-12-2023'