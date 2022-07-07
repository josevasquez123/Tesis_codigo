import stimulus
from pygds import GDS
import multiprocessing, ctypes
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


class SSVEP:

    def __init__(self, name):
        self.name = name
    
    #Metodo que obtiene los datos del EEG cuando se activa la bandera startDataAdq
    def dataAdq(self, startDataAdq, l, n_pruebas):

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

            #Obtencion y guardado de lectura de datos
            data2 = d.GetData(d.SamplingRate*5)             #Esto significa leer por 4 segundos
            data.append(data2)

            #Se limpia la bandera
            l.acquire()
            startDataAdq.value = False
            l.release()

        d.Close()
        del d

        #Guardar data
        cwd = os.getcwd()
        data_path = cwd + '\\' + 'data_17_06\\'
        filename = data_path + self.name + ".npy"
        np.save(filename,data)
        
    #Metodo que inicia el multiproceso, en el cual se activa el metodo dataAdq y la presentacion de los flickers
    def run(self):

        #Se crea el mutex
        l = multiprocessing.Lock()

        #Se crea la variable compartida entre procesos
        startDataAdq = multiprocessing.Value(ctypes.c_int,0)

        #Se crea el objeto que contiene la presentacion de los flickers
        stim = stimulus.stimulus()
        n_pruebas = 4

        #Se definen los procesos con sus respectivas funciones de inicio y parametros
        p1 = multiprocessing.Process(target=self.dataAdq, args=[startDataAdq, l, n_pruebas])
        p2 = multiprocessing.Process(target=stim.runBloque, args=[startDataAdq, l, n_pruebas])

        #Se  inician los procesos
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        

if __name__=="__main__":
    s = SSVEP(name='gary_1')
    s.run()