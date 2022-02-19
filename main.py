import numpy as np
#from ssvep_paradigm import SSVEP
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

if __name__=="__main__":

    """ data = np.load('prueba2.npy')

    data = data.T

    duration = 2

    sampleRate = 256

    N = sampleRate * duration

    x = np.linspace(0, duration, N, endpoint=False)
    
    y = np.sin(10.0 * 2.0*np.pi*x) + np.cos(15.0 * 2.0*np.pi*x) + np.sin(10.0 * 4.0*np.pi*x) + np.sin(15.0 * 4.0*np.pi*x)       #Para verificar que se realizo correctamente el fft
    #y = data[11][3*N:4*N]

    yf = fft(y)
    xf = fftfreq(N, 1 / sampleRate)

    plt.plot(xf, np.abs(yf))
    plt.show() """

    print(np.zeros(4))