import os
import subprocess
import numpy as np
from obspy import read
import matplotlib.pyplot as plt

os.putenv("SAC_DISPLAY_COPYRIGHT", "0")
sacfile = "RM_SACPZ_XO.LT08..HHZ.SAC"
# cut sac files
s = ""
s += "cut t1 -0.5 4.5 \n"
s += "r %s \n" %(sacfile)
s += "w signal.sac \n"
s += "cut t1 -5.5 -0.5 \n"
s += "r %s \n" %(sacfile)
s += "w noise.sac \n"
s += "q \n"
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())

# do fft with SAC and save spectrum files
s = ""
s += "r signal.sac \n"
s += "fft \n"
s += "writesp am signal_spectrum \n"
s += "r noise.sac \n"
s += "fft \n"
s += "writesp am noise_spectrum \n"
s += "q \n"
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())

# plot spectrum and SNR
signal = read("signal_spectrum.am")
noise = read("noise_spectrum.am")
signal_data = signal[0].data
noise_data = noise[0].data
SNR = signal_data/noise_data
npts = signal[0].stats.npts
freq_inc = signal[0].stats.delta
x_axis = []
for i in range(0,npts):
    freq = freq_inc+freq_inc*i
    x_axis.append(freq)

plt.loglog(x_axis,signal_data,'b',linewidth=2,label="signal")
plt.loglog(x_axis,noise_data,'r--',linewidth=1,label="noise")
plt.loglog(x_axis,SNR,'g',linewidth=2,label="SNR")
plt.axhline(y=2,xmin=0.001,xmax=50,label="SNR=2")
plt.legend(loc="best")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Amplitude")
plt.savefig("XO.LT08.pdf")
