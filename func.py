import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import butter, lfilter, freqz
import pygds

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

if __name__=="__main__":
    
    """ data = []

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    filter_data = 25

    d = pygds.GDS()

    pygds.configure_demo(d)
    d.SetConfiguration()

    def animate(i):
        dat = d.GetData(d.SamplingRate)
        dat = np.array(dat.T[3]).flatten()
        dat = dat[filter_data:]
        data.extend(dat)
        ax.cla()
        ax.plot(data)

    
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show() """

    subplots_number = 2

    lists = {}

    fig, axs = plt.subplots(2)
    #fig, axs = plt.subplots(int(subplots_number/2),int(subplots_number/2))

    for i in range(subplots_number):
        lists['l'+str(i)] = []

    avoid_data = 30

    d = pygds.GDS()

    pygds.configure_demo(d)
    d.SetConfiguration()

    def animate(i):
        dat = d.GetData(d.SamplingRate)
        dat = np.array(dat.T)
        c4 = butter_lowpass_filter(dat[3], 30, d.SamplingRate)
        c5 = butter_lowpass_filter(dat[4], 30, d.SamplingRate)
        lists['l0'].extend(c4[avoid_data:])
        lists['l1'].extend(c5[avoid_data:])

        """ for y in range(dat.shape[0]):
            dat[y] = dat[y][filter_data:] """
        
        """ for x in range(subplots_number):
            filter_data = butter_lowpass_filter(dat[x+3][avoid_data:], 30, d.SamplingRate)
            lists['l'+str(x)].extend(filter_data)
            #lists['l'+str(x)].extend(dat[x+3][avoid_data:]) """
        
        axs[0].cla()
        axs[1].cla()
        axs[0].plot(lists['l0'])
        axs[0].set_title('Canal 1')
        #axs[0,1].plot(lists['l1'])
        #axs[0,1].set_title('Canal 2')
        axs[1].plot(lists['l1'])
        axs[1].set_title('Canal 2')
        #axs[1,1].plot(lists['l3'])
        #axs[1,1].set_title('Canal 4')

    
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

