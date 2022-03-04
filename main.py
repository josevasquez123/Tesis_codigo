import numpy as np
from sklearn.cross_decomposition import CCA
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

if __name__=="__main__":

    """ X = [[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [3.,5.,4.]]
    Y = [[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]]
    cca = CCA(n_components=1)
    cca.fit(X, Y)

    X_c, Y_c = cca.transform(X, Y)

    res = np.corrcoef(X_c[:, 0], Y_c[:, 0])

    print(X_c[:,0])
    print(Y_c[:,0]) """

    data = np.load('Gary.npy')

    data = data.T

    duration = 4

    sampleRate = 2400

    N = sampleRate * duration

    x = np.linspace(0, duration, N, endpoint=False)
    
    #y = np.sin(10.0 * 2.0*np.pi*x) + np.cos(15.0 * 2.0*np.pi*x) + np.sin(10.0 * 4.0*np.pi*x) + np.sin(15.0 * 4.0*np.pi*x)       #Para verificar que se realizo correctamente el fft
    y = data[5]

    yf = fft(y)
    xf = fftfreq(N, 1 / sampleRate)

    #plt.plot(x,y)
    plt.plot(xf, np.abs(yf))
    plt.show()
