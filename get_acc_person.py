import signal_processing
import os
import numpy as np

if __name__=="__main__":
    #cwd = os.getcwd()
    #data_path = cwd + '\\' + 'data_17_06\\'
    data = np.load("jose_db.npy")

    d = signal_processing.SignalProcessing(1)
    acc = d.getAcc(data)
    print(acc)