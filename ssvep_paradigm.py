from time import sleep
import stimulus
import multiprocessing, ctypes
from playsound import playsound
from psychopy import core

class SSVEP:
    
    #Metodo que obtiene los datos del EEG cuando se activa la bandera startDataAdq
    def dataAdq(self, startDataAdq, l):
        _startDataAdq = False
        while _startDataAdq==False:
            sleep(0.5)
            l.acquire()
            _startDataAdq = startDataAdq.value
            print(_startDataAdq)
            l.release()
        playsound('ringtone.mp3')
        
        
    #Metodo que inicia el multiproceso, en el cual se activa el metodo dataAdq y la presentacion de los flickers
    def run(self):
        l = multiprocessing.Lock()
        startDataAdq = multiprocessing.Value(ctypes.c_int,0)
        stim = stimulus.stimulus()
        p1 = multiprocessing.Process(target=self.dataAdq, args=[startDataAdq, l])
        p2 = multiprocessing.Process(target=stim.runPrueba, args=[startDataAdq, l])
        p1.start()
        p2.start()
        p1.join()
        p2.join()

if __name__=="__main__":
    s = SSVEP()
    s.run()