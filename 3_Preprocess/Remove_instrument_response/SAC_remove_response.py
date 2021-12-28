import glob
import subprocess
from obspy.core import read


seedfile = glob.glob("XO.*.mseed")
st = read(seedfile[0])
for tr in st:
    fname = "%s.%s.SAC" % (tr.stats.network, tr.stats.station)
    tr.write(fname, format="SAC")
    pz_file = "%s.%s.SAC_PZ" %(tr.stats.network, tr.stats.station)

processed_sac = fname+"_rmpz"
s = ""
s += "r {} \n".format(fname)
s += "rmean; rtr; taper \n"
s += "trans from polezero subtype {} to vel freq 0.001 0.005 35 40\n".format(pz_file)
s += "w %s \n" %(processed_sac)
s += "q \n"
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
