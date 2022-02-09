from time import sleep
import stimulus
import multiprocessing
from playsound import playsound
from psychopy import core

class SSVEP:

    startDataAdq = False
    """ l = multiprocessing.Lock()
    stim = stimulus.stimulus() """
    print("hola")

    def prueba1(self):
        print("hola1")
    
    def prueba2(self):
        print("hola2")

    def dataAdq(self):
        _startDataAdq = False
        while(_startDataAdq==False):
            sleep(0.1)
            self.l.acquire()
            _startDataAdq = self.startDataAdq
            self.l.release()
        
        playsound('ringtone.mp3')
        

    """ def runPrueba(self):

        self.stim.freq_text.draw()
        self.stim.win.flip()
        core.wait(0.9)

        #CADA LOOPEADA ES 1/60 SEGUNDOS, ENTONCES 240 LOOPS SON 4 SEGUNDOS    
        self.l.acquire()
        self.startDataAdq = True
        self.l.release()

        for frameN in range(self.stim.tiempo_adquisicion(4)):
            
            self.stim.flickStimulusFrequency(10,60,frameN,self.stim.rectang)
            self.stim.flickStimulusFrequency(10,60,frameN,self.stim.rectang2)
            self.stim.flickStimulusFrequency(10,60,frameN,self.stim.rectang3)
            self.stim.flickStimulusFrequency(10,60,frameN,self.stim.rectang4)

            self.stim.drawRectangs()
            self.stim.win.flip(clearBuffer=True)

        core.wait(3)
        self.stim.win.close() """
    


    def run(self):
        #s = stimulus.stimulus()
        p1 = multiprocessing.Process(target=self.prueba1)
        p2 = multiprocessing.Process(target=self.prueba2)
        p1.start()
        p2.start()
        p1.join()
        p2.join()

if __name__=="__main__":
    s = SSVEP()
    s.run()