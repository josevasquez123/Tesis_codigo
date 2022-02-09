from psychopy import visual, core

def makeRectang(position, win):
        rect = visual.Rect(win=win, units="pix", width= 384,height =216, pos=position, fillColor="black")
        return rect

class stimulus:

    """ screenWidth = 1536
    screenHeight = 864
    posibles_rectangs = ["Primer rectangulo", "Segundo rectangulo", "Tercer rectangulo", "Cuarto rectangulo"]

    win = visual.Window(color="white", units="pix", size=[screenWidth, screenHeight], waitBlanking=False)
    freq_text = visual.TextStim(win=win, text="HOLA", color="black", height=100)
    rectang = makeRectang([-384,216], win)
    rectang2  = makeRectang([384,216], win)
    rectang3 = makeRectang([-384, -216], win)
    rectang4 = makeRectang([384,-216], win)

    win.mouseVisible = False """

    def getFrameRate(self):
        print(self.win.getActualFrameRate())

    def drawRectangs(self):
        self.rectang.draw()
        self.rectang2.draw()
        self.rectang3.draw()
        self.rectang4.draw()
    
    def opacityRectangs(self, rectangs, opac):
        rectangs.setOpacity(opac)

    def flickStimulusFrequency(self,freq, refresh_rate, frameN, rectangs):
        frame = refresh_rate/freq
        if frameN % frame*2 >= frame:
            self.opacityRectangs(rectangs,0.0)
        else:
            self.opacityRectangs(rectangs,1.0)
    
    def tiempo_adquisicion(self, tiempo):
        return tiempo*60
    
    def runPrueba(self):

        self.freq_text.draw()
        self.win.flip()
        core.wait(0.9)

        #CADA LOOPEADA ES 1/60 SEGUNDOS, ENTONCES 240 LOOPS SON 4 SEGUNDOS    

        for frameN in range(self.tiempo_adquisicion(4)):
            
            self.flickStimulusFrequency(10,60,frameN,self.rectang)
            self.flickStimulusFrequency(10,60,frameN,self.rectang2)
            self.flickStimulusFrequency(10,60,frameN,self.rectang3)
            self.flickStimulusFrequency(10,60,frameN,self.rectang4)

            self.drawRectangs()
            self.win.flip(clearBuffer=True)

        core.wait(3)
    
    def runBloque(self):
        for index in range(2):
            self.freq_text.setText(text=self.posibles_rectangs[index%4])
            self.runPrueba()
        self.win.close()

    def runSesion(self):
        self.runBloque()
        core.wait(5*60)
        self.runBloque()
        core.wait(5*60)
        self.runBloque()
        core.wait(5*60)
        self.runBloque()

if __name__=="__main__":
    stimulus()

