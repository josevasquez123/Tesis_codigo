from numpy import number
from psychopy.visual import Rect, Window, TextStim
from psychopy.core import wait


#FLICKER 12HZ DEBERIA SALIR 12.5 EN LA PRACTICA

class stimulus:

    screenWidth = 1536#1920
    screenHeight = 864#1080
    posibles_rectangs = ["Primer rectangulo", "Segundo rectangulo", "Tercer rectangulo", "Cuarto rectangulo"]
    win = None
    freq_text = None
    rectang1 = rectang2 = rectang3 = rectang4 = None
    freqs = [8,10,12,13]
    
    def init(self):
        self.win = Window(color="white", screen=0,units="pix", size=[stimulus.screenWidth, stimulus.screenHeight], waitBlanking=False)
        self.win.mouseVisible = False
        self.freq_text = TextStim(win=self.win, text="", color="black", height=100)
        self.rectang1 = self.makeRectang([-660,350])
        self.rectang2  = self.makeRectang([660,350])
        self.rectang3 = self.makeRectang([-660, -350])
        self.rectang4 = self.makeRectang([660,-350]) 
    

    def makeRectang(self, position):
        rect = Rect(win=self.win, units="pix", width= 550,height =310, pos=position, fillColor="black")
        return rect


    def runPrueba(self,startDataAdq, l, index):

        l.acquire()
        startDataAdq.value = True
        l.release()

        for frameN in range(self.tiempo_adquisicion(5)):
            
            self.flickStimulusFrequency(self.freqs[index],frameN, self.rectang1)
            self.flickStimulusFrequency(self.freqs[index],frameN, self.rectang2)
            self.flickStimulusFrequency(self.freqs[index],frameN, self.rectang3)
            self.flickStimulusFrequency(self.freqs[index],frameN, self.rectang4)

            self.drawRectangs()
            self.win.flip(clearBuffer=True)

        self.clearRectangs()
        self.drawRectangs()
        self.win.flip(clearBuffer=True)
        wait(4)
    
    def runPruebaOnline(self,startDataAdq, l):
        self.freq_text.setText(text="")
        self.freq_text.draw()
        self.win.flip()
        #wait(2)

        l.acquire()
        startDataAdq.value = True
        l.release()

        """ for frameN in range(self.tiempo_adquisicion(5)):
            
            self.flickStimulusFrequency(8,frameN, self.rectang1)
            self.flickStimulusFrequency(10,frameN, self.rectang2)
            self.flickStimulusFrequency(12,frameN, self.rectang3)
            self.flickStimulusFrequency(15,frameN, self.rectang4)

            self.drawRectangs()
            self.win.flip(clearBuffer=True)

        self.clearRectangs()
        self.drawRectangs()
        self.win.flip(clearBuffer=True)
        wait(4) """

    
    def showText(self, text):
        self.freq_text.setText(text=text)
        self.freq_text.draw()
        self.win.flip()
        wait(2)
        self.freq_text.setText(text="")
        self.freq_text.draw()
        self.win.flip()
        wait(1)

    def drawRectangs(self):
        self.rectang1.draw()
        self.rectang2.draw()
        self.rectang3.draw()
        self.rectang4.draw()
    
    def clearRectangs(self):
        self.rectang1.setOpacity(0.0)
        self.rectang2.setOpacity(0.0)
        self.rectang3.setOpacity(0.0)
        self.rectang4.setOpacity(0.0)

    def flickStimulusFrequency(self,freq, frameN, rectangN):
        frame = 60/(freq*2)
        if frameN % (frame*2) >= frame:
            rectangN.setOpacity(1.0)
        else:
            rectangN.setOpacity(0.0)
    
    def tiempo_adquisicion(self, tiempo):
        return tiempo*60

    def runBloque(self, startDataAdq, l, numPruebas):

        for index in range(numPruebas):
            self.init()
            self.showText(stimulus.posibles_rectangs[index%4])
            self.runPrueba(startDataAdq, l, index%4)
            self.win.close()
        
    def runPruebaEV(self, startDataAdq, l, numPruebas):
        l.acquire()
        startDataAdq.value = True
        l.release()

        """ for index in range(numPruebas):
            self.init()
            self.runPruebaOnline(startDataAdq, l)
            self.win.close() """
        
    
    def getFrameRate(self):
        win_frame = Window(color="white", screen=1,units="pix", size=[stimulus.screenWidth, stimulus.screenHeight], waitBlanking=False)
        print(win_frame.getActualFrameRate())
    
    def runTest(self):

        self.init()

        for frameN in range(self.tiempo_adquisicion(10)):
            
            self.flickStimulusFrequency(10,frameN, self.rectang1)
            self.flickStimulusFrequency(10,frameN, self.rectang2)
            self.flickStimulusFrequency(12,frameN, self.rectang3)
            self.flickStimulusFrequency(15,frameN, self.rectang4)

            self.drawRectangs()
            self.win.flip(clearBuffer=True)
    
    def runBloqueTest(self):
        for loop in range(1):
            self.runTest()
            wait(2)
        
    def checkPositions(self):
        self.win = Window(color="white", screen=1,units="pix", size=[stimulus.screenWidth, stimulus.screenHeight], waitBlanking=False)
        self.win.mouseVisible = False
        self.rectang1 = self.makeRectang([-660,350])
        self.rectang2  = self.makeRectang([660,350])
        self.rectang3 = self.makeRectang([-660, -350])
        self.rectang4 = self.makeRectang([660,-350]) 

        self.rectang1.draw()
        self.rectang2.draw()
        self.rectang3.draw()
        self.rectang4.draw()

        self.win.flip()
        wait(10)

if __name__=="__main__":
    s = stimulus()
    s.runTest()

