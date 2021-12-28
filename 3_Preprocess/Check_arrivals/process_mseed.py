import os
import glob
from obspy import read, read_inventory
from obspy.core import UTCDateTime


def pre_process(station_name):
    inv_name = "./stations/*.%s.xml" %(station_name)
    inv = read_inventory(inv_name)
    mseed_list = glob.glob("./%s/*.mseed" %(station_name))
    if len(mseed_list) == 0:
        pass
    else:
        for mseed in mseed_list[0:9]:
            mseed = mseed.strip()
            sac_name = mseed.replace("mseed","SAC",1)
            st = read(mseed)
            tr = st[0]
            pre_filt = [0.001,0.005,20,30]
            new_st = st.copy()
            new_tr = new_st[0]
            new_tr = tr.remove_response(inventory=inv,pre_filt=pre_filt,\
                                        output="VEL")
            new_st.write(sac_name,format="SAC")
    
            stream = read(sac_name)
            trace = stream[0]
            event_id = sac_name.split("/")[-1].split("_")[0]
            staname = sac_name.split("/")[-1].split("_")[2]
            cmd1 = "cat %s.list | awk '/%s/ {print $2}'" %(staname,event_id)
            origintime = os.popen(cmd1).read().strip()
            print(origintime)
            origintime = UTCDateTime(origintime)
            cmd2 = "cat %s.list | awk '/%s/ {print $4}'" %(staname,event_id)
            arrival_time = os.popen(cmd2).read().strip()
            arrival_time = UTCDateTime(arrival_time)
            traveltime = arrival_time-origintime
            trace.stats.sac.t1 = traveltime+60
            stream.write(sac_name,format="SAC")


station_list = ["KD04","KS11","KD12","EP15","EP23","LT08","LT11","LD36","WD59"]
for station in station_list:
    print(station)
    pre_process(station)
