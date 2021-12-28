import os
import glob
import numpy as np
from obspy import read
from mtspec import mtspec
import matplotlib.pyplot as plt


def cal_spectrum_for_single_event_station(sacfile):

    # calculate spectrum of a single event and station pair.

    # parameters for mtspec and sampling_rate=40Hz 
    npts = 200
    time_bandwidth = 3.5
    ntapers = 5
    twin_start = -0.5

    event_id = os.getcwd().split("/")[-2]
    st = read(sacfile)
    tr = st[0]
    P_wave_arrival = tr.stats.sac.t1
    delta = tr.stats.delta

    window_timestamp = tr.stats.starttime+P_wave_arrival+twin_start
    noise_window_start = window_timestamp-(npts-1)*delta
    signal_window_end = window_timestamp+(npts-1)*delta
    tr_noise = tr.copy().trim(noise_window_start, window_timestamp)
    tr_signal = tr.copy().trim(window_timestamp, signal_window_end)

    noise_spec,f_noise = mtspec(tr_noise, delta, time_bandwidth, \
                                number_of_tapers=ntapers)
    signal_spec,f_signal = mtspec(tr_signal, delta, time_bandwidth, \
                           number_of_tapers=ntapers)
    snr = signal_spec/noise_spec
    
    # parameters for mtspec and sampling_rate=100Hz 
    npts = 500
    time_bandwidth = 3.5
    ntapers = 5
    twin_start = -0.5

    delta = 0.01
    sampling_rate = int(1.0/delta)
    new_tr = tr.copy().resample(sampling_rate=sampling_rate)
    new_window_timestamp = tr.stats.starttime+P_wave_arrival+twin_start
    new_noise_window_start = new_window_timestamp-(npts-1)*delta
    new_signal_window_end = new_window_timestamp+(npts-1)*delta
    new_tr_noise = new_tr.copy().trim(new_noise_window_start, new_window_timestamp)
    new_tr_signal = new_tr.copy().trim(new_window_timestamp, new_signal_window_end)
    new_noise_spec, new_f_noise = mtspec(new_tr_noise, delta, time_bandwidth, \
                                         number_of_tapers=ntapers)

    new_signal_spec, new_f_signal = mtspec(new_tr_signal, delta, time_bandwidth, \
                                         number_of_tapers=ntapers)
    new_snr = new_signal_spec/new_noise_spec


    # plot seismogram 
    plt.figure(figsize=(12,5))
    plt.subplot(221)
    plot_time = tr.times()-P_wave_arrival
    plot_noise_time = tr_noise.times()+twin_start-(npts-1)*delta
    plot_signal_time = tr_signal.times()+twin_start
    plt.plot(plot_time,tr.data,"gray",linewidth=1.5)
    plt.plot(plot_noise_time,tr_noise.data,"blue",linewidth=1.5,label="noise")
    plt.plot(plot_signal_time,tr_signal.data,"red",linewidth=1.5,label="signal")
    plt.xlim(-10,10)
    plt.xlabel("Time relative to P arrival time (s)")
    figure_title = event_id+" "+sacfile
    plt.title(figure_title)
    plt.legend(loc="best")


    # plot spectral signal-to-noise ratio 
    plt.subplot(223)
    plt.loglog(f_signal,snr,'green',linewidth=2,label="SNR")
    plt.loglog(new_f_signal,new_snr,'red',linewidth=2,label="resample_SNR")
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("SNR")
    plt.axhline(y=2,xmin=0.001,xmax=50,label="SNR=2")
    plt.ylim(1,100000)
    plt.legend(loc="best")

    # plot P-wave spectra
    plt.subplot(122)
    plt.loglog(f_noise,noise_spec,"g--",linewidth=2,label="noise")
    plt.loglog(f_signal,signal_spec,"green",linewidth=2,label="signal")
    plt.loglog(new_f_noise,new_noise_spec,"r--",linewidth=2,label="resample_noise")
    plt.loglog(new_f_signal,new_signal_spec,"red",linewidth=2,label="resample_signal")
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("Spectral Amplitude")
    plt.axvline(20)
    plt.legend(loc="best")

    plt.tight_layout()
    figure_name = sacfile.replace("SAC",".resample.pdf")
    plt.savefig(figure_name)


sac_list = glob.glob("*.SAC")
for sacfile in sac_list:
    cal_spectrum_for_single_event_station(sacfile)
