import os
from obspy import read_events


def get_pick_info(quakemlfile):
    cata = read_events(quakemlfile)
    with open("picks.dat", "w") as fpick:
        for event in cata:
            event_id = event.preferred_origin_id.id.split("/")[-1]
            origin_time = event.origins[0].time
            for pick in event.picks:
                network = pick.waveform_id.network_code
                station = pick.waveform_id.station_code
                channel = pick.waveform_id.channel_code
                location = pick.waveform_id.location_code
                sta_info = network+"_"+station+"_"+channel+"_"+location
                pick_time = pick.time
                fpick.write("{} {} {} {}\n".format(
                             event_id,
                             origin_time,
                             sta_info,
                             pick_time))
    fpick.close()

quakemlfile = "./catalog/*/*.quakeml"
get_pick_info(quakemlfile)           
