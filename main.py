import socket
from pygds import GDS
import multiprocessing, ctypes
import signal_processing
import stimulus
import time
import time
import numpy as np
import os

def config_usbamp(d, samplingRate= 256,notch_index=-1, BP_index=-1, acquire=1):
    d.Counter = 0
    d.Trigger = 0
    d.SamplingRate = samplingRate

    for ch in d.Channels:
        ch.Acquire = acquire
        ch.BandpassFilterIndex = BP_index
        ch.NotchFilterIndex = notch_index
        ch.BipolarChannel = 0  # 0 => to GND

    d.ShortCutEnabled = 0
    d.CommonGround = [1]*4
    d.CommonReference = [1]*4

    d.NumberOfScans_calc()

    if(acquire!=0):
        d.SetConfiguration()


class BCI:

    s = None

    def dataAdq(self, startDataAdq, l, n_pruebas, s):

        d = GDS()
        config_usbamp(d)

        _startDataAdq = False

        data = []

        for loops in range(n_pruebas):
            #Esperar hasta que la bandera indique el inicio de lectura de datos
            while _startDataAdq==False:
                l.acquire()
                _startDataAdq = startDataAdq.value
                l.release()

            print("inicio!!!!!!!!!!!")
            time.sleep(2)
            data2 = d.GetData(d.SamplingRate*5)             
            data.append(data2)
            #time.sleep(5)
            

            #Se limpia la bandera
            l.acquire()
            startDataAdq.value = False
            l.release()
        
        #cwd = os.getcwd()
        #data_path = cwd + '\\' + 'data_01_06\\'
        #x = np.load(data_path+"paolo_yt_1p_10hz.npy")
        temp = signal_processing.SignalProcessing()
        mov = temp.runSignalProcessing(data)
        msg = f"done,{str(mov)}"
        self.s.send(msg.encode())
        self.s.close()
        d.Close()
        del d

        #Guardar data
        #cwd = os.getcwd()
        #data_path = cwd + '\\' + 'data_07_06\\'
        #filename = data_path + "prueba_online.npy"
        #np.save(filename,data)


    def initSocketConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        port = 1755            
        self.s.connect(('10.100.108.27', port))
        data_to_send = "OK"
        self.s.send(data_to_send.encode())
        while True:
            data_serv = self.s.recv(1024).decode('UTF-8')
            if data_serv == "OK":
                return True
    
    def testEVMovements(self, mov):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        port = 1755            
        self.s.connect(('192.168.18.11', port))
        data = f"done,{str(mov)}"
        self.s.send(data.encode())

    def run(self):
        connection_status = False
        while(connection_status==False):
            connection_status = self.initSocketConnection()
        
        l = multiprocessing.Lock()

        startDataAdq = multiprocessing.Value(ctypes.c_int,0)

        stim = stimulus.stimulus()

        n_pruebas = 1

        #Se definen los procesos con sus respectivas funciones de inicio y parametros
        p1 = multiprocessing.Process(target=self.dataAdq, args=[startDataAdq, l, n_pruebas, self.s])
        p2 = multiprocessing.Process(target=stim.runPruebaEV, args=[startDataAdq, l,n_pruebas])

        #Se  inician los procesos
        p1.start()
        p2.start()
        p1.join()
        p2.join()

if __name__=="__main__":
    s = BCI()
    #s.run()
    time.sleep(2)
    s.testEVMovements(2)
