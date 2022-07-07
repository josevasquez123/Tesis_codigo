import matplotlib.pyplot as plt
from scipy.fft import fft
import numpy as np
import time

data = np.load('signals.npy')
N = 4*256
n = np.arange(N)
sr = 256
T = N/sr
freq = n/T 
n_oneside = N//2
f_oneside = freq[:n_oneside]

plt.ion() 

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [])

ln.set_xdata(f_oneside)

temp = 0
while True:
    try:
        ydata = data[temp:temp+N]
        temp = temp + N
        ydata = fft(ydata)
        ydata = np.abs(ydata[:n_oneside])
        ln.set_ydata(ydata)

        ax.relim()
        ax.autoscale_view()
        ax.set_xticks(np.arange(min(f_oneside), max(f_oneside)+1, 1.0))
        ax.set_xlim([0,30])

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(3)
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
        break