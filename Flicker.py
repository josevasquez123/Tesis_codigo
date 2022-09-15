from psychopy.visual import Rect, Window, TextStim
from psychopy.core import wait


#TIP: PARA ENTENDER EL CODIGO DEBES LEER LA LIBRERIA PSYCHOPY, TAMBIEN EXISTE FOROS DE PSYCHOPY
#EV: ENTORNO VIRTUAL (MI CASO: EL BRAZO ROBOTICO)

class stimulus:

    screenWidth = 1536#1920
    screenHeight = 864#1080
    posibles_rectangs = ["Primer rectangulo", "Segundo rectangulo", "Tercer rectangulo", "Cuarto rectangulo"]
    win = None
    freq_text = None
    rectang1 = rectang2 = rectang3 = rectang4 = None
    freqs = [8,10,12,13]        #FRECUENCIAS UTILIZADAS EN LOS FLICKERS
    
    def init(self):
        self.win = Window(color="white", screen=0,units="pix", size=[stimulus.screenWidth, stimulus.screenHeight], waitBlanking=False)
        self.win.mouseVisible = False
        self.freq_text = TextStim(win=self.win, text="", color="black", height=100)
        
        #CREACION DE 4 RECTANGULOS
        self.rectang1 = self.makeRectang([-660,350])
        self.rectang2  = self.makeRectang([660,350])
        self.rectang3 = self.makeRectang([-660, -350])
        self.rectang4 = self.makeRectang([660,-350]) 
    

    def makeRectang(self, position):
        rect = Rect(win=self.win, units="pix", width= 550,height =310, pos=position, fillColor="black")
        return rect

    #EXPOSICION DE FLICKERS PARA UNA PRUEBA
    def runPrueba(self,startDataAdq, l, index):

        #BLOQUEO DE LOS PROCESOS
        l.acquire()
        #SETEO COMO TRUE LA VARIABLE COMPARTIDA PARA QUE EL OTRO PROCESO EMPIECE SU FUNCIONAMIENTO
        startDataAdq.value = True
        #DESBLOQUEO LOS PROCESOS
        l.release()

        #MUESTRO LOS 4 FLICKERS POR EL TIEMPO INDICADO EN LA FUNCION TIEMPO_ADQUISICION
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
        #ESPERO 4 SEGUNDOS DESPUES QUE SE HAYA ACABADO LA EXPOSICION DE LOS FLICKERS PARA QUE LA PERSONA DESCANSE
        #ESTE ES EL TIEMPO DE DESCANSO ENTRE PRUEBAS!
        wait(4)

    def showText(self, text):
        self.freq_text.setText(text=text)
        self.freq_text.draw()
        self.win.flip()
        #ACA CONTROLAS CUANTO TIEMPO QUIERES QUE SE MUESTRE EL TEXTO EN LA PANTALLA
        wait(2)
        self.freq_text.setText(text="")
        self.freq_text.draw()
        self.win.flip()
        #ACA CONTROLAS CUANTO TIEMPO QUIERES DARLE AL PACIENTE PARA QUE SE PREPARE PARA OBSERVAR LOS FLICKERS
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

    #FUNCION QUE GENERA LOS FLICKERS
    #FREQ = FRECUENCIA DEL FLICKER
    #RECTANGN = RECTANGULO A REALIZAR LOS CAMBIOS
    #FRAMEN = EL NUMERO DE FRAME ACTUAL
    def flickStimulusFrequency(self,freq, frameN, rectangN):
        #60 ES DEBIDO A QUE LA PANTALLA QUE UTILICE ES DE 60 FPS
        #ESTO ES ALGO COMPLICADO DE EXPLICAR PERO ESTA EN PSYCHOPY PARA QUE LO ENTIENDAS,EN RESUMEN ES UNA FORMULA
        #PARA MAYOR INFORMACION, BUSCAR ESTOS PAPERS:
        #VISUAL STIMULUS DESIGN FOR HIGH-RATE SSVEP BCI
        #Generating visual flickers for eliciting robust steady-state visual evoked potentials at flexible frequencies using monitor refresh rate
        frame = 60/(freq*2)
        if frameN % (frame*2) >= frame:
            rectangN.setOpacity(1.0)
        else:
            rectangN.setOpacity(0.0)
    
    #EL TIEMPO ESTA EN FUNCION DE LOS FPS, POR ESO EN MI CASO (PANTALLA DE 60FPS) EL TIEMPO QUE QUIERO LO MULTIPLICO POR 60
    def tiempo_adquisicion(self, tiempo):
        return tiempo*60

    #EJECUTO DE MANERA SECUENCIAL LAS PRUEBAS (BLOQUE = UN NUMERO DE PRUEBAS O BLOCK = MANY TRIALS)
    def runBloque(self, startDataAdq, l, numPruebas):
        
        #NUMPRUEBAS = NUMERO DE PRUEBAS POR BLOQUE QUE QUIERAS REALIZAR
        for index in range(numPruebas):
            self.init()
            #ACA MUESTRO EL RECTANGULO QUE DEBE OBSERVAR EL PACIENTE EN LA PRUEBA, ES UN TEXTO GIGANTE QUE APARECERA EN LA PANTALLA
            self.showText(stimulus.posibles_rectangs[index%4])
            self.runPrueba(startDataAdq, l, index%4)
            self.win.close()

    #EJECUTA LA PRUEBA ONLINE
    def runPruebaOnline(self,startDataAdq, l):
        self.freq_text.setText(text="LISTO?")
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

    #EJECUTA UN BLOQUE DE PRUEBAS EN EL MODO ONLINE (CUANDO QUIERES CONTROLAR EL EV)
    def runPruebaEV(self, startDataAdq, l, numPruebas):
        l.acquire()
        startDataAdq.value = True
        l.release()

        #NUMPRUEBAS = CANTIDAD DE PRUEBAS ONLINE QUE DESEES
        """ for index in range(numPruebas):
            self.init()
            self.runPruebaOnline(startDataAdq, l)
            self.win.close() """
        
    #CODIGO PARA OBTENER LOS FPS DE TU PANTALLA
    def getFrameRate(self):
        win_frame = Window(color="white", screen=1,units="pix", size=[stimulus.screenWidth, stimulus.screenHeight], waitBlanking=False)
        print(win_frame.getActualFrameRate())
    
    #TESTEO RAPIDO PARA VERIFICAR LA CALIDAD DE LOS FLICKERS CREADOS
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
        
    #TESTEO RAPIDO PARA VER SI ESTAN EN LA UBICACION CORRECTA O SI TIENEN EL TAMAÑO CORRECTO LOS FLICKERS
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

