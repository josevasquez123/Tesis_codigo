import numpy as np
from sklearn.cross_decomposition import CCA
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import scipy.fftpack as fourier

if __name__=="__main__":

    """ X = [[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [3.,5.,4.]]
    Y = [[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]]
    cca = CCA(n_components=1)
    cca.fit(X, Y)

    X_c, Y_c = cca.transform(X, Y)

    res = np.corrcoef(X_c[:, 0], Y_c[:, 0])

    print(X_c[:,0])
    print(Y_c[:,0]) """

    """ data = np.load('Gary.npy')

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
    plt.show() """

    FRAMES = 2      #Cantidad de datos en una lectura

    fig, (ax,ax1) = plt.subplots(2)

    x_audio = np.arange(0,FRAMES,1)
    x_fft = np.linspace(0, Fs, FRAMES)

    line, = ax.plot(x_audio, np.random.rand(FRAMES),'r')
    line_fft, = ax1.semilogx(x_fft, np.random.rand(FRAMES), 'b')

    ax.set_ylim(-32500,32500)
    ax.ser_xlim = (0,FRAMES)

    Fmin = 1
    Fmax = 5000
    ax1.set_xlim(Fmin,Fmax)

    fig.show()


    F = (Fs/FRAMES)*np.arange(0,FRAMES//2)                 # Creamos el vector de frecuencia para encontrar la frecuencia dominante

    while True:
        
        data = stream.read(FRAMES)                         # Leemos paquetes de longitud FRAMES
        dataInt = struct.unpack(str(FRAMES) + 'h', data)   # Convertimos los datos que se encuentran empaquetados en bytes
        
        line.set_ydata(dataInt)                            # Asignamos los datos a la curva de la variación temporal
        
        M_gk = abs(fourier.fft(dataInt)/FRAMES)            # Calculamos la FFT y la Magnitud de la FFT del paqute de datos
        #M_gk = fft(y)

        
        ax1.set_ylim(0,np.max(M_gk+10)) 
        line_fft.set_ydata(M_gk)                           # Asigmanos la Magnitud de la FFT a la curva del espectro 
        
        M_gk = M_gk[0:FRAMES//2]                           # Tomamos la mitad del espectro para encontrar la Frecuencia Dominante
        Posm = np.where(M_gk == np.max(M_gk))
        F_fund = F[Posm]                                   # Encontramos la frecuencia que corresponde con el máximo de M_gk
        
        print(int(F_fund))                                 # Imprimimos el valor de la frecuencia dominante

        fig.canvas.draw()
        fig.canvas.flush_events()
