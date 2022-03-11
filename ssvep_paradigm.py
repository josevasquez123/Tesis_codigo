from datetime import date
import stimulus
from pygds import GDS
from gtec import gtec
import multiprocessing, ctypes
from numpy import save as saveEEGSignals


class SSVEP:

    #data=[]

    def __init__(self, name):
        self.name = name
    
    #Metodo que obtiene los datos del EEG cuando se activa la bandera startDataAdq
    def dataAdq(self, startDataAdq, l):

        d = GDS()
        gtec.config_usbamp(d)

        _startDataAdq = False

        #Esperar hasta que la bandera indique el inicio de lectura de datos
        while _startDataAdq==False:
            l.acquire()
            _startDataAdq = startDataAdq.value
            l.release()

        #Obtencion y guardado de lectura de datos
        data2 = d.GetData(d.SamplingRate*4)          #Esto significa leer por 4 segundos
        filename = self.name+".npy"
        saveEEGSignals(filename, data2)
        """ global data
        dataTemp = d.GetData(d.SamplingRate*4)          #Esto significa leer por 4 segundos
        data.append(dataTemp) """

        d.Close()
        del d

        #Se limpia la bandera
        l.acquire()
        startDataAdq.value = False
        l.release()
        
    #Metodo que inicia el multiproceso, en el cual se activa el metodo dataAdq y la presentacion de los flickers
    def run(self):

        #Se crea el mutex
        l = multiprocessing.Lock()

        #Se crea la variable compartida entre procesos
        startDataAdq = multiprocessing.Value(ctypes.c_int,0)

        #Se crea el objeto que contiene la presentacion de los flickers
        stim = stimulus.stimulus()

        #Se definen los procesos con sus respectivas funciones de inicio y parametros
        p1 = multiprocessing.Process(target=self.dataAdq, args=[startDataAdq, l])
        p2 = multiprocessing.Process(target=stim.runBloque, args=[startDataAdq, l, 1])

        #Se  inician los procesos
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        """ #Guardar la data
        filename = 'prueba' + self.name + '.npy'

        global data
        
        saveEEGSignals(filename, data) """
        

if __name__=="__main__":
    s = SSVEP(name='GaryGa2')
    s.run()