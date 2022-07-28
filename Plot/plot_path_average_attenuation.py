import os
import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


data = np.loadtxt("atten.dat")
cmap = plt.cm.jet
norm = mpl.colors.Normalize(vmin=0, vmax=4)
new_jet = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, project="3d")
pstar_data = glob.glob("./workdir/*_pstar027.dat")
for event in pstar_data:
    orid = event.split("/")[-1].split("_")[0]
    fevent = open(event, "r")
    stalst = fevent.readlines()
    for sta in stalst:
        sta = sta.strip()
        evla = float(sta.split()[1])
        evlo = float(sta.split()[2])
        evdp = float(sta.split()[3])
        atten = float(sta.split()[-1])
        sta_name = sta.split()[0]
        cmd = "awk '/%s/ {print}' ./stainfo.dat" %(staname)
        output = os.popen(cmd).read().strip()
        stlo = float(output.split()[2])
        stla = float(output.split()[3])
        