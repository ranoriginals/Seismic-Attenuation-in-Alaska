from glob import glob
from obspy import read_inventory

def get_stainfo(xmlfile):
    inv = read_inventory(xmlfile)
    net = inv[0]
    sta = net[0]
    lat = sta.latitude
    lon = sta.longitude
    net_name = xmlfile.split(".")[0]
    sta_name = xmlfile.split(".")[1]
    if "Z" in sta[0].code:
        cha = sta[0]
    elif "Z" in sta[1].code:
        cha = sta[1]
    else:
        cha = sta[2]
    cha_name = cha.code
    sample_rate = cha.sample_rate
    print(xmlfile,sample_rate,lon,lat)

xmlfile_list = glob("*.xml")
for xmlfile in xmlfile_list:
    get_stainfo(xmlfile)
