from psychopy import visual, core

class stimulus:

    screenWidth = 1536
    screenHeight = 864
    posibles_rectangs = ["Primer rectangulo", "Segundo rectangulo", "Tercer rectangulo", "Cuarto rectangulo"]
    

    def runPrueba(self, win, freq_text, rectang1, rectang2, rectang3, rectang4,startDataAdq, l):

        #Inicio mostrando el cuadrado que debe ver (la pista)
        freq_text.draw()
        win.flip()
        core.wait(0.9)

        l.acquire()
        startDataAdq.value = True
        l.release()

        #CADA LOOPEADA ES 1/60 SEGUNDOS, ENTONCES 240 LOOPS SON 4 SEGUNDOS 

        #Inicia los parpadeos de los 4 rectangulos a las frecuencias definidas
        for frameN in range(self.tiempo_adquisicion(4)):
            
            self.flickStimulusFrequency(10,60,frameN,rectang1)
            self.flickStimulusFrequency(10,60,frameN,rectang2)
            self.flickStimulusFrequency(10,60,frameN,rectang3)
            self.flickStimulusFrequency(10,60,frameN,rectang4)

            self.drawRectangs(rectang1, rectang2, rectang3, rectang4)
            win.flip(clearBuffer=True)

        core.wait(3)

    def makeRectang(self, position, win):
        rect = visual.Rect(win=win, units="pix", width= 384,height =216, pos=position, fillColor="black")
        return rect

    def drawRectangs(self, rectang1, rectang2, rectang3, rectang4):
        rectang1.draw()
        rectang2.draw()
        rectang3.draw()
        rectang4.draw()
    
    def opacityRectangs(self, rectangs, opac):
        rectangs.setOpacity(opac)

    def flickStimulusFrequency(self,freq, refresh_rate, frameN, rectangN):
        frame = refresh_rate/freq
        if frameN % frame*2 >= frame:
            self.opacityRectangs(rectangN,0.0)
        else:
            self.opacityRectangs(rectangN,1.0)
    
    def tiempo_adquisicion(self, tiempo):
        return tiempo*60

    def runBloque(self, startDataAdq, l, numPruebas):

        #Inicializacion de todo los objetos del GUI de los estimulos SSVEP
        win = visual.Window(color="white", units="pix", size=[stimulus.screenWidth, stimulus.screenHeight], waitBlanking=False)
        freq_text = visual.TextStim(win=win, text="", color="black", height=100)
        win.mouseVisible = False
        rectang1 = self.makeRectang([-384,216], win)
        rectang2  = self.makeRectang([384,216], win)
        rectang3 = self.makeRectang([-384, -216], win)
        rectang4 = self.makeRectang([384,-216], win)

        for index in range(numPruebas):
            freq_text.setText(text=stimulus.posibles_rectangs[index%4])
            self.runPrueba(win, freq_text, rectang1, rectang2, rectang3, rectang4, startDataAdq, l)
        
        win.close()
        
    def runSesion(self):
        self.runBloque()
        core.wait(5*60)
        self.runBloque()
        core.wait(5*60)
        self.runBloque()
        core.wait(5*60)
        self.runBloque()
    
    def getFrameRate(self, win):
        print(win.getActualFrameRate())

if __name__=="__main__":
    s = stimulus()
    s.runPrueba()

