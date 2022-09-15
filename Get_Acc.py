import signal_processing
import numpy as np

if __name__=="__main__":
    data = np.load("jose_db.npy")

    d = signal_processing.SignalProcessing(1)
    acc = d.getAcc(data)
    print(acc)