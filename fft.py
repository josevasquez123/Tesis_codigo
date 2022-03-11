import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.fft import fft, fftfreq
import pygds

d = pygds.GDS()

pygds.configure_demo(d)
d.SetConfiguration()

plt.ion() # Stop matplotlib windows from blocking

# Setup figure, axis and initiate plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [])

avoid_data = 30

duration = 1
N= d.SamplingRate * duration

x = np.linspace(0, duration, N, endpoint=False)
xf = fftfreq(N, 1 / d.SamplingRate)
ln.set_xdata(xf)

while True:
    time.sleep(1)

    # Get the new data
    ydata = d.GetData(d.SamplingRate)
    ydata = np.array(ydata.T)
    ydata = ydata[4]
    ydata = np.abs(fft(ydata))
    #xdata = np.arange(10)
    #ydata = np.random.random(10)

    # Reset the data in the plot
    #ln.set_xdata(xdata)
    ln.set_ydata(ydata)
    ax.set_ylim(0,np.max(ydata+10)) 

    # Rescale the axis so that the data can be seen in the plot
    # if you know the bounds of your data you could just set this once
    # so that the axis don't keep changing
    ax.relim()
    ax.autoscale_view()

    # Update the window
    fig.canvas.draw()
    fig.canvas.flush_events()