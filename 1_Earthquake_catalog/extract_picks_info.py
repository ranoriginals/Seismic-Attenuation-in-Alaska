import os
from obspy import read_events

# read quakeml files and extract picks information

def get_pick_info(quakemlfile):
    catalog = read_events(quakemlfile)
    with open("picks.dat", "w") as fpick:
        for event in catalog:
            event_id = event.resource_id.id.split("/")[-1]
            origin_time = event.origins[0].time
            for i in range(len(event.picks)):
                pick = event.picks[i]
                arrival = event.origins[0].arrivals[i]
                if pick.resource_id == arrival.pick_id:
                    net = pick.waveform_id.network_code
                    sta = pick.waveform_id.station_code
                    loc = pick.waveform_id.location_code
                    cha = pick.waveform_id.channel_code
                    pick_time = pick.time
                    pick_phase = arrival.phase
                    stainfo = net+"."+sta+"."+loc+"."+cha
                    stainfo = stainfo.ljust(15," ")
                    fpick.write("{} {} {} {} {} \n".format(
                        event_id,
                        origin_time,
                        stainfo,
                        pick_time,
                        pick_phase)
                    )
    fpick.close()
    
get_pick_info("*.quakeml")
