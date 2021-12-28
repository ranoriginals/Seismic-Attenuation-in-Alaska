import os
import glob
import numpy as np
from obspy import read
from mtspec import mtspec
from mtspec import sine_psd
import matplotlib.pyplot as plt

# parameters for mtspec
npts = 500
time_bandwidth = 3.5
ntapers = 5
twin_start = -0.5

def cal_spectrum_for_single_event_station(sacfile):

    # calculate spectrum of a single event and station pair.

    event_id = os.getcwd().split("/")[-1]
    st = read(sacfile)
    tr = st[0]
    P_wave_arrival = tr.stats.sac.t0
    delta = tr.stats.delta

    window_timestamp = tr.stats.starttime+P_wave_arrival+twin_start
    noise_window_start = window_timestamp-(npts-1)*delta
    signal_window_end = window_timestamp+(npts-1)*delta
    tr_noise = tr.copy().trim(noise_window_start, window_timestamp)
    tr_signal = tr.copy().trim(window_timestamp, signal_window_end)

    # mtspec 
    noise_spec,f_noise = mtspec(tr_noise, delta, time_bandwidth, \
                                number_of_tapers=ntapers)
    signal_spec,f_signal = mtspec(tr_signal, delta, time_bandwidth, \
                           number_of_tapers=ntapers)
    snr = signal_spec/noise_spec

    # sine_psd
    sine_noise_spec, sine_f_noise = sine_psd(tr_noise, delta)
    sine_signal_spec, sine_f_signal = sine_psd(tr_signal, delta)
    sine_snr = sine_signal_spec/sine_noise_spec

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
    plt.loglog(sine_f_signal, sine_snr, 'red', linewidth=2, label="sine_SNR")
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("SNR")
    plt.axhline(y=2,xmin=0.001,xmax=50,label="SNR=2")
    plt.ylim(1,100000)
    plt.legend()

    # plot P-wave spectra
    plt.subplot(122)
    plt.loglog(f_noise,noise_spec,"b--",linewidth=2,label="noise")
    plt.loglog(f_signal,signal_spec,"b",linewidth=2,label="signal")
    plt.loglog(sine_f_noise, sine_noise_spec,"r--", linewidth=2, label="sine_noise")
    plt.loglog(sine_f_signal, sine_signal_spec, "r", linewidth=2, label="sine_signal")
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("Spectral Amplitude")
    plt.legend()

    plt.tight_layout()
    figure_name = sacfile.replace("SAC","pdf")
    plt.savefig(figure_name)

sac_list = glob.glob("*.SAC")
for sacfile in sac_list:
    cal_spectrum_for_single_event_station(sacfile)
