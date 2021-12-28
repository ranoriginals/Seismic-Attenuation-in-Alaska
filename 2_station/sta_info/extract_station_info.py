import os
import glob

def get_stainfo(xmlfile):
    net_name = xmlfile.split(".")[0]
    sta_name = xmlfile.split(".")[1]
    cmd_lon = "cat %s | awk '/Longitude/ {print}' | head -1 | \
               awk -F '<' '{print $2}' | awk -F '>' '{print $2}'" \
               %(xmlfile)
    sta_lon = os.popen(cmd_lon).read().strip()
    cmd_lat = "cat %s | awk '/Latitude/ {print}' | head -1 | \
               awk -F '<' '{print $2}' | awk -F '>' '{print $2}'" \
               %(xmlfile)
    sta_lat = os.popen(cmd_lat).read().strip()

    return net_name, sta_name, sta_lon, sta_lat


xml_list = glob.glob("*.xml")
with open("stainfo.dat",'w') as fsta: 
    for xmlfile in xml_list:
        net_name, sta_name, sta_lon, sta_lat = get_stainfo(xmlfile)
        fsta.write("{} {} {} {}\n".format(net_name, sta_name, sta_lon, sta_lat))
fsta.close()
