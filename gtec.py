import pygds
import matplotlib.pyplot as plt
import time
import numpy as np
from scipy.fft import fft, fftfreq
from itertools import count
from matplotlib.animation import FuncAnimation

class gtec():

    def config_usbamp(d, samplingRate= 2400,notch_index=11, BP_index=148, acquire=1):
        d.Counter = 0
        d.Trigger = 0
        d.SamplingRate = samplingRate

        for ch in d.Channels:
            ch.Acquire = acquire
            ch.BandpassFilterIndex = BP_index
            ch.NotchFilterIndex = notch_index
            ch.BipolarChannel = 0  # 0 => to GND

        d.ShortCutEnabled = 0
        d.CommonGround = [1]*4
        d.CommonReference = [1]*4

        d.NumberOfScans_calc()

        if(acquire!=0):
            d.SetConfiguration()
    
    def animate(i, d, y):
        data = d.GetData(d.SamplingRate)
        
        y.extend(np.squeeze(data.T))

        #print(y)
        #x = np.linspace(x_axis_timing, x_axis_timing+1, d.SamplingRate, endpoint=False)

        #print(i)

        plt.cla()

        plt.plot(y)

        plt.tight_layout()


    def show_one_channel_v2(d, channel):

        gtec.config_usbamp(d, acquire=0, notch_index=3, BP_index=45, samplingRate=256)

        d.Channels[channel-1].Acquire = 1

        d.SetConfiguration()

        plt.style.use('fivethirtyeight')

        y = []

        anim = FuncAnimation(plt.gcf(), gtec.animate, interval=1100, fargs=(d, y))

        plt.tight_layout()
        plt.show()

    def show_one_channel(d, channel):

        gtec.config_usbamp(d, acquire=0)

        d.Channels[channel-1].Acquire = 1

        d.SetConfiguration()

        scope = pygds.Scope(1/d.SamplingRate, xlabel='t/s', ylabel=u'V/μV',
                  title=f'Channel {channel}')

        d.GetData(d.SamplingRate, more=scope)

        d.Close()
        del d
    
    def show_one_channel_fft(d, channel, duration=1):
        
        gtec.config_usbamp(d, acquire=0)

        d.Channels[channel-1].Acquire = 1

        d.SetConfiguration()

        plt.ion() # Stop matplotlib windows from blocking

        # Setup figure, axis and initiate plot
        fig, ax = plt.subplots()
        xdata, ydata = [], []
        ln, = ax.plot([], [])

        duration = duration

        sampleRate = d.SamplingRate

        N = sampleRate * duration

        while True:
            time.sleep(1)

            # Get the new data
            xdata = np.linspace(0, duration, N, endpoint=False)
            ydata = d.GetData(d.SamplingRate)
            ydata = ydata.T

            #ydata = ydata[channel-1:channel]

            ydata = np.abs(fft(ydata))
            xdata = fftfreq(N, 1 / sampleRate)

            # Reset the data in the plot
            ln.set_xdata(xdata)
            ln.set_ydata(ydata)

            # Rescale the axis so that the data can be seen in the plot
            # if you know the bounds of your data you could just set this once
            # so that the axis don't keep changing
            ax.relim()
            ax.set_xlim([-60,60 ])
            ax.set_ylim([0, 0.15e8])
            #ax.set_xlim(5,30)
            #ax.autoscale_view()

            # Update the window
            fig.canvas.draw()
            fig.canvas.flush_events()


    #BUSCAR LOS INDICES DE LOS CANALES PARA DEFINIRLOS EN EL SUBPLOTS
    def show_all_channels(d):

        gtec.config_usbamp(d)

        scope = pygds.Scope(1/d.SamplingRate, subplots={0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14, 15:15},modal=False,
                  ylabel=(u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV', u'U/μV',u'U/μV')
                  , xlabel=('t/s','t/s','t/s','t/s', 't/s','t/s','t/s','t/s', 't/s','t/s','t/s','t/s', 't/s','t/s','t/s','t/s')
                  , title=('Ch1', 'Ch2','Ch3', 'Ch4', 'Ch5', 'Ch6','Ch7', 'Ch8', 'Ch9', 'Ch10','Ch11', 'Ch12', 'Ch13', 'Ch14','Ch15', 'Ch16')
                  )

        d.GetData(d.SamplingRate, more=scope)
        d.Close()
        del d

    def save_data(name, d, duration):
        filename = name+".npy"

        gtec.config_usbamp(d)

        data = d.GetData(d.SamplingRate*duration)

        np.save(filename, data)
    
    

        
        
