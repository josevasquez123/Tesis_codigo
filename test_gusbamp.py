import pygds
from gtec import gtec

#d.NumberOfScans_calc() setea el NumberOfScans como 8, tomando en cuenta el SampleRate

#BP Filtro SR: 2400hz, Index: 148, LcutFreq: 0hz, UcutFreq: 30hz
#N Filtro SR: 2400hz, Index: 11, LcutFreq: 58hz, UcutFreq: 62


if __name__=="__main__":

    d = pygds.GDS()

    gtec.save_data("garlic3",d,5)
    
    #gtec.show_one_channel_v2(d, 5)

    #print(d.GetBandpassFilters())


#bp 45
#notch 3

    