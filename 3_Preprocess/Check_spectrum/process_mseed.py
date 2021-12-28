import os
import glob
import subprocess
from obspy import read
from obspy import UTCDateTime
from obspy.clients.iris import Client


def mseed_to_sac(mseedfile):
    st = read(mseedfile)
    tr = st[0]
    fname = "%s.%s.%s.%s.SAC" % (tr.stats.network, tr.stats.station, \
                                 tr.stats.location, tr.stats.channel)
    tr.write(fname,format="SAC")

def get_response(mseedfile):
    st = read(mseedfile)
    tr = st[0]
    net = tr.stats.network
    sta = tr.stats.station
    loc = tr.stats.location
    cha = tr.stats.channel
    starttime = UTCDateTime(tr.stats.starttime)
    endtime = UTCDateTime(tr.stats.endtime)
    sacpz_filename = "SAC_PZ_"+net+"_"+sta+"_"+cha
    client = Client()
    sacpz = client.sacpz(net,sta,loc,cha,starttime,endtime,sacpz_filename)


def remove_response(SACfile,SAC_PZ,rm_sacpz_filename):
    s = ""
    s += "r %s \n" %(SACfile)
    s += "rmean; rtr; taper \n"
    s += "trans from polezero subtype %s to vel freq 0.001 0.005 90 100 \n" %(SAC_PZ)
    s += "mul 1.0e9 \n"
    s += "w %s \n" %(rm_sacpz_filename)
    s += "q \n"
    subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())

def mark_arrival(picks_file,rm_sacpz_filename):
    st = read(rm_sacpz_filename)
    tr = st[0]
    net = tr.stats.network
    sta = tr.stats.station
    loc = tr.stats.location
    cha = tr.stats.channel
    event_match_string = os.getcwd().split("/")[-1]
    sta_match_string = net+"_"+sta+"_"+cha
    origintime = os.popen("cat %s | awk '/%s/ {print}' | awk '/%s/ {print $2}'"\
                          %(picks_file,event_match_string,sta_match_string)) \
                          .read().strip()
    origintime = UTCDateTime(origintime)
    arrivaltime = os.popen("cat %s | awk '/%s/ {print}' | awk '/%s/ {print $4}'"\
                          %(picks_file,event_match_string,sta_match_string)) \
                          .read().strip()
    arrivaltime = UTCDateTime(arrivaltime)
    traveltime = arrivaltime-origintime
    tr.stats.sac.t1 = traveltime+60
    print(tr.stats.sac.t1)
    st.write(rm_sacpz_filename,format="SAC")


mseedfile_list = glob.glob("*.mseed")
picks_file = "/mnt/home/zhuoran/Waveform-check/picks.dat"
for mseedfile in mseedfile_list:
    mseed_sp = mseedfile.split(".")
    net = mseed_sp[0]
    sta = mseed_sp[1]
    cha = mseed_sp[2]
    loc = mseed_sp[3]
    mseed_to_sac(mseedfile)
    get_response(mseedfile)
    SACfile = net+"."+sta+"."+loc+"."+cha+".SAC"
    SAC_PZ = "SAC_PZ_"+net+"_"+sta+"_"+cha
    rm_sacpz_filename = "RM_SACPZ_"+SACfile
    remove_response(SACfile,SAC_PZ,rm_sacpz_filename)
    mark_arrival(picks_file,rm_sacpz_filename)
