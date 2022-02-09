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
    
    

        
        
