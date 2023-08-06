import numpy as np
import json
import scipy.signal
from iqube.default_config import *

class DataPreparation:
    def __init__(self,key, attribute):  # key = "to_plot", attribute = "error_signal_1"
        self.key = key
        self.attribute = attribute

    def data_import_json(self, path):
        with open(path) as json_file:
            obj = json.load(json_file)
            data_str = obj[self.key][self.attribute]
        return np.array(data_str)

    def data_import_csv(self, path):
        array = np.loadtxt(path, delimiter=",",dtype = str,unpack=True)
        return array

class SpectrumAnalysis:
    def __init__(self, data):
        self.data = data

    def filtering(self, f_ny, p_kHz):
        data = self.data
        p = p_kHz/f_ny
        b, a = scipy.signal.butter(2, p)
        signal = scipy.signal.filtfilt(b, a, data)
        noise = data - signal
        return signal, noise


    def calc_snr(self, signal, noise, l1, l2):
        [i_max,peak], [i_min,valley], midpoint = determine_transition_data(signal, l1,l2)

        width = 10
        if (midpoint-l1 >= width) & (midpoint-l1 + width+1 <= len(signal)):
            dy = signal[midpoint - width] - signal[midpoint + width]
        else:
            dy = 0
        print(dy)
        slope2noise = np.abs(float(dy / np.std(noise)))
        signal2noise = float((peak - valley) / np.std(noise))
        return signal2noise,slope2noise

def determine_transition_data(signal, l1,l2):
    L = np.size(signal)
    if (l2 < L) & (l1 >= 0):
        y = signal[int(l1):int(l2)]
        i_max = np.argmax(y)
        i_min = np.argmin(y)
        peak = signal[int(i_max+l1)]
        valley = signal[int(i_min+l1)]
        midpoint = int((2*l1+i_max + i_min) / 2)

        return [i_max,peak],[i_min,valley], midpoint
    else:
        print("Error: Edges need to be inside the data region!")
        return [0,0], [0,0],0

def path_to_data(path, p_kHz):
    data = DataPreparation("to_plot",
                               attribute = "error_signal_1").data_import_json(path)
    f_ny = 59/2*np.size(data)/1000  # 59 Hz * Number of Samples / 2 /1000 yields the Nyquist-frequency in kHz
    width = 200
    cutoff_data = data[width:-width]  # Cutting of edges because of errorenous data
    signal,noise = SpectrumAnalysis(cutoff_data).filtering(f_ny,p_kHz)
    return cutoff_data, signal, noise

def basic_plot(ax,data,x_index,y_index, color, label):

    x = np.array(data[x_index])
    y = np.array(data[y_index])
    line1, = ax.plot(x, y, linestyle="none", marker="x", label=label, markercolor = color)
    ax.set_xlabel(description_fields[x_index])
    ax.set_ylabel(description_fields[y_index])