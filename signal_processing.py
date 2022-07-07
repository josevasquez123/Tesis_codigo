import numpy as np
from scipy.signal import butter, lfilter
from sklearn.cross_decomposition import CCA
from operator import itemgetter


class SignalProcessing:

    target_freqs = [6,10,8,15]
    sr = 256
    avoid_data = 30
    length_signal_w = sr*5-avoid_data
    length_signal = sr*5

    def __init__(self,step):
        self.step = step

    def butter_bandpass(self,lowcut, highcut, fs, order=5):
        return butter(order, [lowcut, highcut], fs=fs, btype='band')

    def bandpass_filter(self,data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y
        
    def get_corr(self,data_eeg, model_signals):
        cca = CCA(n_components=1)
        len_result = model_signals.shape[0]
        results = dict(zip(self.target_freqs,np.zeros(len_result)))

        for index in np.arange(len_result):
            #model_signal_temp = model_signals[index].reshape(-1,1)
            cca.fit(data_eeg.T, model_signals[index,:,:].T)
            O1_a,O1_b = cca.transform(data_eeg.T, model_signals[index,:,:].T)
            results[self.target_freqs[index]] = np.corrcoef(O1_a[:,0],O1_b[:,0])[0,1]
        
        return results

    def getReferenceSignal(self,length, target_freq, samplingRate):
        # generate sinusoidal reference templates for CCA for the first and second harmonics
        reference_signals = []
        t = np.arange(0, (length/(samplingRate)), step=1.0/(samplingRate))
        #First harmonics/Fundamental freqeuncy
        reference_signals.append(np.sin(np.pi*2*target_freq*t))
        reference_signals.append(np.cos(np.pi*2*target_freq*t))
        #Second harmonics
        reference_signals.append(np.sin(np.pi*4*target_freq*t))
        reference_signals.append(np.cos(np.pi*4*target_freq*t))
        reference_signals = np.array(reference_signals)
        return reference_signals
    
    def getReferenceSignals(self):
        freq1 = self.getReferenceSignal(self.length_signal_w,self.target_freqs[0],self.sr)
        freq2 = self.getReferenceSignal(self.length_signal_w,self.target_freqs[1],self.sr)
        freq3 = self.getReferenceSignal(self.length_signal_w,self.target_freqs[2],self.sr)
        freq4 = self.getReferenceSignal(self.length_signal_w,self.target_freqs[3],self.sr)
        freqs = np.array([freq1,freq2,freq3,freq4])
        
        return freqs
    
    def Preprocessing(self,data):
        xs = np.squeeze(data)
        xs = xs.T
        ref = xs[2][self.avoid_data:]
        #xs_O1 = xs[7][30:] - ref 
        xs_O2 = xs[10][self.avoid_data:] - ref
        xs_Oz = xs[15][self.avoid_data:] - ref
        xs_POz = xs[14][self.avoid_data:] - ref
        xs_PO4 = xs[13][self.avoid_data:] - ref
        xs_PO3 = xs[12][self.avoid_data:] - ref

        #xs_O1_mean = xs_O1 - np.mean(xs_O1)
        xs_O2_mean = xs_O2 - np.mean(xs_O2)
        xs_Oz_mean = xs_Oz - np.mean(xs_Oz)
        xs_POz_mean = xs_POz - np.mean(xs_POz)
        xs_PO3_mean = xs_PO3 - np.mean(xs_PO3)
        xs_PO4_mean = xs_PO4 - np.mean(xs_PO4)

        #xs_O1_norm = (xs_O1_mean-np.min(xs_O1_mean))/(np.max(xs_O1_mean)-np.min(xs_O1_mean))
        xs_O2_norm = (xs_O2_mean-np.min(xs_O2_mean))/(np.max(xs_O2_mean)-np.min(xs_O2_mean))
        xs_Oz_norm = (xs_Oz_mean-np.min(xs_Oz_mean))/(np.max(xs_Oz_mean)-np.min(xs_Oz_mean))
        xs_POz_norm = (xs_POz_mean-np.min(xs_POz_mean))/(np.max(xs_POz_mean)-np.min(xs_POz_mean))
        xs_PO3_norm = (xs_PO3_mean-np.min(xs_PO3_mean))/(np.max(xs_PO3_mean)-np.min(xs_PO3_mean))
        xs_PO4_norm = (xs_PO4_mean-np.min(xs_PO4_mean))/(np.max(xs_PO4_mean)-np.min(xs_PO4_mean))

        data_eeg_norm = np.array([xs_O2_norm, xs_Oz_norm, xs_POz_norm, xs_PO3_norm, xs_PO4_norm])

        xs_Oz_filtered = self.bandpass_filter(xs_Oz_norm,5,32,256,9)
        xs_POz_filtered = self.bandpass_filter(xs_POz_norm,5,32,256,9)
        xs_PO3_filtered = self.bandpass_filter(xs_PO3_norm,5,32,256,9)
        xs_PO4_filtered = self.bandpass_filter(xs_PO4_norm,5,32,256,9)
        #xs_O1_filtered = self.bandpass_filter(xs_O1_norm,6,32,256,9)
        xs_O2_filtered = self.bandpass_filter(xs_O2_norm,5,32,256,9)

        data_eeg = np.array([xs_Oz_filtered, xs_O2_filtered, xs_PO3_filtered, xs_PO4_filtered, xs_POz_filtered])
        return data_eeg
    
    def getMaxCorr(self,corr):
        maxCorr = max(corr.items(), key=itemgetter(1))[0]
        if(maxCorr==self.target_freqs[0]):
            return 1
        elif(maxCorr==self.target_freqs[1]):
            return 2
        elif(maxCorr==self.target_freqs[2]):
            return 3
        elif(maxCorr==self.target_freqs[3]):
            return 4
    
    def getMaxFreq(self,corr):
        return max(corr.items(), key=itemgetter(1))[0]
    
    def runSignalProcessing(self, data):
        data_eeg = self.Preprocessing(data)
        referenceSignals = self.getReferenceSignals()
        res = self.get_corr(data_eeg, referenceSignals) 
        mov = self.getMaxCorr(res)
        return mov

    def ventana(self,data):
        all_data = []
        all_data2 = []
        for index in range(len(data)):
            temp = []
            temp2 = []
            for steps in range(round(len(data[index])/(self.sr*self.step))):
                if(steps==0):
                    temp.append(data[index][int(self.sr*self.step*steps):int(self.sr*self.step*(steps+1))-30])
                else:
                    if self.step<3:
                        temp2.append(data[index][int(self.sr*self.step*steps)-30:int(self.sr*self.step*(steps+1))-30])
            all_data.append(temp)    
            if temp2:
                all_data2.append(temp2)
        return np.array(all_data), np.array(all_data2)
    
    def filtrado(self,data):
        data_filtered = []
        for index in range(data.shape[0]):
            temp = []
            for index_electrode in range(data[index].shape[0]):
                temp2 = self.bandpass_filter(data[index][index_electrode],5,32,256,9)
                temp.append(temp2)
            data_filtered.append(temp)

        return np.array(data_filtered)
    
    def getReferenceSignalsVentanadas(self,length_signal):
        freq1 = self.getReferenceSignal(length_signal,self.target_freqs[0],self.sr)
        freq2 = self.getReferenceSignal(length_signal,self.target_freqs[1],self.sr)
        freq3 = self.getReferenceSignal(length_signal,self.target_freqs[2],self.sr)
        freq4 = self.getReferenceSignal(length_signal,self.target_freqs[3],self.sr)
        freqs = np.array([freq1,freq2,freq3,freq4])
        
        return freqs
    
    def PreprocessingOffline(self,data):
        xs = np.squeeze(data)
        xs = xs.T
        ref = xs[2][30:]
        xs_O2 = xs[10][30:] - ref
        xs_Oz = xs[15][30:] - ref
        xs_POz = xs[14][30:] - ref
        xs_PO4 = xs[13][30:] - ref
        xs_PO3 = xs[12][30:] - ref


        #xs_O1_mean = xs_O1 - np.mean(xs_O1)
        xs_O2_mean = xs_O2 - np.mean(xs_O2)
        xs_Oz_mean = xs_Oz - np.mean(xs_Oz)
        xs_POz_mean = xs_POz - np.mean(xs_POz)
        xs_PO3_mean = xs_PO3 - np.mean(xs_PO3)
        xs_PO4_mean = xs_PO4 - np.mean(xs_PO4)

        #xs_O1_norm = (xs_O1_mean-np.min(xs_O1_mean))/(np.max(xs_O1_mean)-np.min(xs_O1_mean))
        xs_O2_norm = (xs_O2_mean-np.min(xs_O2_mean))/(np.max(xs_O2_mean)-np.min(xs_O2_mean))
        xs_Oz_norm = (xs_Oz_mean-np.min(xs_Oz_mean))/(np.max(xs_Oz_mean)-np.min(xs_Oz_mean))
        xs_POz_norm = (xs_POz_mean-np.min(xs_POz_mean))/(np.max(xs_POz_mean)-np.min(xs_POz_mean))
        xs_PO3_norm = (xs_PO3_mean-np.min(xs_PO3_mean))/(np.max(xs_PO3_mean)-np.min(xs_PO3_mean))
        xs_PO4_norm = (xs_PO4_mean-np.min(xs_PO4_mean))/(np.max(xs_PO4_mean)-np.min(xs_PO4_mean))

        data_eeg_norm = np.array([xs_O2_norm, xs_Oz_norm, xs_POz_norm, xs_PO3_norm, xs_PO4_norm])

        temp, temp2 = self.ventana(data_eeg_norm)

        n_ventanados_2 = round(self.length_signal/(self.sr*self.step))-1
        n_datos = int(self.sr*self.step)-30
        n_datos_2 = int(self.sr*self.step)

        temp = temp.reshape(1,5,n_datos)
        if temp2.size>0:
            temp2 = temp2.reshape(n_ventanados_2,5,n_datos_2)

        temp = self.filtrado(temp)
        if temp2.size>0:
            temp2 = self.filtrado(temp2)
        
        return temp, temp2
    
    def getAcc(self,data):
        num_aciertos = 0
        num_aciertos_freqs = [0,0,0,0]
        num_pruebas = len(data)
        referenceSignals = self.getReferenceSignals()
        for index in range(num_pruebas):
            data_temp = self.Preprocessing(data[index])
            res = self.get_corr(data_temp,referenceSignals)
            freq_predicha = self.getMaxFreq(res)
            if(freq_predicha==self.target_freqs[index%4]):
                num_aciertos += 1
                num_aciertos_freqs[index%4] += 1
        print(num_aciertos_freqs)
        return num_aciertos/num_pruebas*100
    
    def getAccVentanado(self,data):
        num_aciertos = 0
        num_pruebas = len(data)
        num_ventanado = 0
        for index in range(num_pruebas):
            data_temp, data_temp2 = self.PreprocessingOffline(data[index])
            if data_temp2.size>0:
                num_ventanado = data_temp.shape[0] + data_temp2.shape[0]
                referenceSignals2 = self.getReferenceSignalsVentanadas(data_temp2.shape[2])
            else:
                num_ventanado = data_temp.shape[0]
            referenceSignals = self.getReferenceSignalsVentanadas(data_temp.shape[2])
            for ventanado_index in range(data_temp.shape[0]):
                vent = data_temp[ventanado_index]
                res = self.get_corr(vent, referenceSignals)
                freq_predicha = self.getMaxFreq(res)
                if(freq_predicha == self.target_freqs[index%4]):
                    num_aciertos += 1
            if data_temp2.size>0:
                for ventanado_index in range(data_temp2.shape[0]):
                    vent = data_temp2[ventanado_index]
                    res = self.get_corr(vent, referenceSignals2)
                    freq_predicha = self.getMaxFreq(res)
                    if(freq_predicha == self.target_freqs[index%4]):
                        num_aciertos += 1
        return num_aciertos/(num_pruebas*num_ventanado)*100






