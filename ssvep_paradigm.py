import stimulus
from pygds import GDS
from gtec import gtec
import multiprocessing, ctypes
from numpy import save as saveEEGSignals


class SSVEP:
    
    #Metodo que obtiene los datos del EEG cuando se activa la bandera startDataAdq
    def dataAdq(self, startDataAdq, l):

        x = GDS()
        _startDataAdq = False

        #Esperar hasta que la bandera indique el inicio de lectura de datos
        while _startDataAdq==False:
            l.acquire()
            _startDataAdq = startDataAdq.value
            l.release()
        #Inicio de lectura de datos
        data2 = x.GetData(x.SamplingRate*4)          #Esto significa leer por 4 segundos

        #Se limpia la bandera
        l.acquire()
        startDataAdq.value = False
        l.release()

        filename = 'prueba2.npy'
        
        saveEEGSignals(filename, data2)
        
        
    #Metodo que inicia el multiproceso, en el cual se activa el metodo dataAdq y la presentacion de los flickers
    def run(self):
        #Envio de la configuracion del GUSBAMP
        d = GDS()
        gtec.configure_Gusbamp(d, 2400, 11, 148)

        d.Close()
        del d

        #Variable donde se guardara las señales EEG
        #data = []

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
        

if __name__=="__main__":
    s = SSVEP()
    s.run()