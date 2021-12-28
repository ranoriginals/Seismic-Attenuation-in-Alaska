from glob import glob
from obspy import read_inventory

def mkdir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def get_stainfo(xmlfile):
    mkdir("./response_figure")
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
    response = cha.response
    response_figure = "./response_figure/"+net_name+"."+sta_name+"."+cha_name+".png"
    response.plot(min_freq=0.001, output="VEL", outfile=response_figure)

xmlfile_list = glob("*.xml")
for xmlfile in xmlfile_list:
    get_stainfo(xmlfile)
