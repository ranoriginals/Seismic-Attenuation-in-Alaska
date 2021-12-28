import os
import glob
from obspy import read
from obspy import read_inventory

'''
def remove(seedfile,water_level):
    seed_sp = seedfile.split(".")
    net = seed_sp[0]
    sta = seed_sp[1]
    cha = seed_sp[2]
    stationxml = "../../Alaska_data/stations/"+net+"."+sta+".xml"
    inv = read_inventory(stationxml).select(channel="??Z")
    st = read(seedfile)
    st_copy = st.copy()
    st_copy.detrend("linear")
    tr_copy = st_copy[0]
    pre_filt = [0.001,0.005,35,40]
    tr_copy.remove_response(inventory=inv,output="VEL",water_level=water_level,\
                            pre_filt=pre_filt,zero_mean=True,taper=True)
    sac_name = net+"."+sta+"."+cha+"."+"water"+str(water_level)+".SAC"
    st_copy.write(sac_name,format="SAC")

seed_list = glob.glob("*.mseed")
water_level_list = [60,100,500,5000,10000]
for seed in seed_list:
    for water_level in water_level_list:
        remove(seed,water_level)
'''

def remove(seedfile):
    seed_sp = seedfile.split(".")
    net = seed_sp[0]
    sta = seed_sp[1]
    cha = seed_sp[2]
    stationxml = "../../Alaska_data/stations/"+net+"."+sta+".xml"
    inv = read_inventory(stationxml).select(channel="??Z")
    st = read(seedfile)
    st_copy = st.copy()
    st_copy.detrend("linear")
    tr_copy = st_copy[0]
    pre_filt = [0.001,0.005,35,40]
    tr_copy.remove_response(inventory=inv,output="VEL",\
                            pre_filt=pre_filt,zero_mean=True,taper=True)
    sac_name = net+"."+sta+"."+cha+".SAC"
    st_copy.write(sac_name,format="SAC")

seed_list = glob.glob("*.mseed")
for seed in seed_list:
    remove(seed)
