import numpy as np
#from ssvep_paradigm import SSVEP
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

if __name__=="__main__":

    data = np.load('prueba2.npy')

    data = data.T

    duration = 4

    sampleRate = 256

    N = sampleRate * duration

    x = np.linspace(0, duration, N, endpoint=False)
    
    #y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)                #Para verificar que se realizo correctamente el fft
    #y = data[15]

    yf = fft(y)
    xf = fftfreq(N, 1 / sampleRate)

    plt.plot(xf, np.abs(yf))
    plt.show()
    
    """ plt.plot(x,y)

    plt.show() """

    #print(y.shape)