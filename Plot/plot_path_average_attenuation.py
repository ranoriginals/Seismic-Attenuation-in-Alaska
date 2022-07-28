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
        ax.scatter(evlo, evla, evdp, marker="o", s=2, alpha=0.5, color="black", label="Events")
        ax.scatter(stlo, stla, 0, marker="^", s=2, alpha=0.5, color="black", label="Stations")
        x = [evlo, stlo]
        y = [evla, stla]
        z = [evdp, 0]
        ax.plot(x, y, z, c=new_jet.to_rgba(atten), linewidth=0.5)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Depth (Km)")
ax.invert_zaxis()
l = 0.9
b = 0.25
w = 0.02
h = 0.6
rect = [l,b,w,h]
cbar_ax = fig.add_axes(rect)
fig.colorbar(new_jet, orientation="vertical", label="1000/Qp", cbar=cbar_ax)
ax.view_init(elev=10, azim=120)
fig.suptitle("Trench Parallel")
plt.savefig("Trench_parallel.pdf")
ax.view_init(elev=10, azim=-150)
fig.suptitle("Trench Normal")
plt.savefig("Trench_normal.pdf")
