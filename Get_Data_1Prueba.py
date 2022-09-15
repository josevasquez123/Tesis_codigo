import pygds
import numpy as np

def config_usbamp(d, samplingRate= 256,notch_index=-1, BP_index=-1, acquire=1):
    d.Counter = 0
    d.Trigger = 0
    d.SamplingRate = samplingRate

    for ch in d.Channels:
        ch.Acquire = acquire
        ch.BandpassFilterIndex = BP_index
        ch.NotchFilterIndex = notch_index
        ch.BipolarChannel = 0  # 0 => to GND

    d.ShortCutEnabled = 0
    d.CommonGround = [1]*4
    d.CommonReference = [1]*4

    d.NumberOfScans_calc()

    if(acquire!=0):
        d.SetConfiguration()

def save_data(name, d, duration):
    filename = name+".npy"

    config_usbamp(d)

    data = d.GetData(d.SamplingRate*duration)

    np.save(filename, data)

if __name__=="__main__":

    d = pygds.GDS()
    save_data("jose_60",d,5)