import pygds
from gtec import gtec
from numpy import array

def demo_channels():
    d = pygds.GDS()
    # configure
    pygds.configure_demo(d, testsignal=d.DeviceType != pygds.DEVICE_TYPE_GUSBAMP)
    d.Counter = 1
    # set configuration
    d.SetConfiguration()
    # get data
    data = d.GetData(d.SamplingRate)
    # plot second channel
    scope = pygds.Scope(1/d.SamplingRate, modal=True, ylabel=u'U/μV',
                  xlabel='t/s', title='Channel 15')
    scope(data[:, 14:15])
    # or
    # plt.plot(data[1:,1])
    #plt.title('Channel 2')
    pygds.plt.show()
    # close
    d.Close()
    del d

#d.NumberOfScans_calc() setea el NumberOfScans como 8, tomando en cuenta el SampleRate
#Indice 39 y 43 son indices de filtro pasa banda de 0.01 y 30, 0.5 y 30 respesctivamente

#Indice 3 para notchfilter

#BP Filtro SR: 2400hz, Index: 148, LcutFreq: 0hz, UcutFreq: 30hz
#N Filtro SR: 2400hz, Index: 11, LcutFreq: 58hz, UcutFreq: 62


if __name__=="__main__":

    filename = 'demo_save.npy'
    dfromfile = pygds.np.load(filename)
    print(array(dfromfile).shape)
    #d = pygds.GDS()
    """ pygds.configure_demo(d)
    d.SetConfiguration() """
    #gtec.configure_Gusbamp(d, 2400, 11, 148)
    #print(d.Configs)
    """ data=[]
    filename = 'demo_save.npy'
    for i in range(4):
        dat = d.GetData(d.SamplingRate)
        data.append(dat)
    
    pygds.np.save(filename, data) """

    """ scope = pygds.Scope(1/d.SamplingRate, modal=True, ylabel=u'U/μV',
                  xlabel='t/s', title='Channel 14')
    scope(data[:, 7:8])
    pygds.plt.show() """


    """ for i in d.GetNotchFilters():
        for x in i:
            print(x) """

    """ filename = 'demo_save.npy'
    assert not pygds.os.path.exists(
        filename), "the file %s must not exist yet" % filename
    #sr = d.GetSupportedSamplingRates()          #Te muestra los sampling rate que soporta el g.usbamp """
   

    
    """ # configure
    pygds.configure_demo(d, testsignal=d.DeviceType != pygds.DEVICE_TYPE_GUSBAMP)
    d.Counter = 1
    # set configuration
    d.SetConfiguration()
    # get data
    data = d.GetData(d.SamplingRate)
    
    #Ploteo de data
    
    scope = pygds.Scope(1/d.SamplingRate, modal=True, ylabel=u'U/μV',
                  xlabel='t/s', title='Channel 14')
    scope(data[:, 14:15])
    pygds.plt.show() """
    

    #Muestra la data de 16x256, cada objeto hace referencia a un canal
    '''
    for i in data.T:
        print(i)
    #print(data.shape)
    '''

    '''
    for i in d.GetNotchFilters():
        for x in i:
            print(x)
    '''

    '''
    for i in d.GetBandpassFilters():
        for x in i:
            print(x)
    #print(d.GetBandpassFilters())
    '''
    
    """ #Te muestra la configuracion de los canales
    for e, i in enumerate(d.Channels):
        print(str(i)+str(e)) """
    