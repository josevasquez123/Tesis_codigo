from msilib.schema import File
import numpy as np

if __name__=="__main__":

    """ z = np.array([[1,2],[3,4]])
    w = np.array([[5,6],[7,8]])
    #print(z.shape)
    print(np.concatenate((z,w),axis=0).T) """

    filename = "demo_save.npy"
    dataFile = np.array(np.load(filename))
    dataResult = dataFile[0]

    for index, data in enumerate(dataFile):  
        if index == 0:
            pass
        else:
            dataResult = np.concatenate((dataResult,data), axis=0)

    print(dataResult.T.shape)