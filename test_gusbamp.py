import pygds
from gtec import gtec
import numpy as np

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

    #pygds.demo_di()

    """ d = pygds.GDS()
    gtec.configure_Gusbamp(d, 2400, 11, 148) """

    dat = np.load('prueba.npy')

    print(dat.shape)

    """ data=[]
    filename = 'demo_save.npy'
    for i in range(4):
        dat = d.GetData(d.SamplingRate)
        data.append(dat)
    
    pygds.np.save(filename, data) """

    """ scope = pygds.Scope(1/d.SamplingRate, subplots={0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15},modal=False,
                  ylabel=(u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV')
                  , xlabel=('t/s','t/s','t/s','t/s', 't/s','t/s','t/s','t/s', 't/s','t/s','t/s','t/s', 't/s','t/s','t/s','t/s')
                  , title=('Ch1', 'Ch2','Ch3', 'Ch4', 'Ch5', 'Ch6','Ch7', 'Ch8', 'Ch9', 'Ch10','Ch11', 'Ch12', 'Ch13', 'Ch14','Ch15', 'Ch16')
                  )

    d.GetData(d.SamplingRate, more=scope) """

    """ filename = 'garyData.npy'

    data = d.GetData(d.SamplingRate*10)

    np.save(filename, data) """



    """ scope = pygds.Scope(1/d.SamplingRate, modal=True, ylabel=u'U/μV',
                  xlabel='t/s', title='Channel 14')
    scope(data[:, 14:15])
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
    