import signal_processing
import numpy as np

if __name__=="__main__":
    
    data = np.load("all_db.npy")

    accs = []
    steps = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]

    for index in range(len(steps)):
        x = signal_processing.SignalProcessing(steps[index])
        acc = x.getAccVentanado(data)
        accs.append(acc)
    
    print(accs)