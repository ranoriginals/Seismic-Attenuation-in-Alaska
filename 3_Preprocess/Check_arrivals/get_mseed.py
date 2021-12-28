import os


def mkdir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def search_list(list_name,staname):
    flist = open(list_name,'r')
    flist_lines = flist.readlines()
    new_list = []
    for line in flist_lines:
        line = line.strip()
        line_sp = line.split()
        stainfo = line_sp[2]
        if staname in line_sp[2] and "HZ" in line_sp[2]:
            new_list.append(line)
    
    new_file = staname+".list"
    with open(new_file,"w") as fnew:
        for i in range(len(new_list)):
            fnew.write(new_list[i]+"\n")
    fnew.close()
    
    return new_list


def get_data(station_name):
    seed_list = search_list("picks.dat",station_name)
    mkdir(station_name)
    data_path = "/mnt/research/seismo_wei/DTian/AACSE/data/waveforms"
    for seed_info in seed_list:
        event_id = seed_info.split()[0]
        stainfo = seed_info.split()[2]
        seed_file = data_path+"/"+event_id+"/"+"*."+station_name+".*HZ.*"
        new_seed_file = "./"+station_name+"/"+event_id+"_"+stainfo+".mseed"
        os.system("cp %s ./%s" %(seed_file,new_seed_file))


station_list = ["KD04","KS11","KD12","EP15","EP23","LT08","LT11","LD36","WD59"]
for station in station_list:
    print(station)
    get_data(station)
