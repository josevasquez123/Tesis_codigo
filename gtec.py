import pygds

class gtec():

    def configure_Gusbamp(d, samplingRate, notchIndex, BPindex):
        pygds.configure_demo(d, testsignal=False)

        for c in d.Configs:
            c.SamplingRate = samplingRate
            for ch in c.Channels:
                ch.BandpassFilterIndex = BPindex
                ch.NotchFilterIndex = notchIndex
        d.NumberOfScans_calc()
        d.SetConfiguration()

    #BUSCAR LOS INDICES DE LOS CANALES PARA DEFINIRLOS EN EL SUBPLOTS
    def showAllChannels(d):
        scope = pygds.Scope(1/d.SamplingRate, subplots={0: 0, 1: 1}, xlabel=(
        '', 't/s'), ylabel=(u'V/μV', 'DI'), title=('Ch1', 'DI'))

        d.GetData(d.SamplingRate, more=scope)
    
    

        
        
