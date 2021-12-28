#!/bin/bash
# plot the distributions of stations (detailed version)

region="-165/-145/51/61"
projection="M16c"

gmt begin station_sample_rate pdf A+m0.5c
gmt basemap -R$region -J$projection -Ba2 -BWSen 
gmt grdimage -R$region -J$projection @earth_relief_01m -I+d
cat sample_rate.dat | awk -F ' ' '{if($2==100) print$3,$4}' | gmt plot -St0.4c -W1p -Ggold1
cat sample_rate.dat | awk -F ' ' '{if($2==50) print$3,$4}' | gmt plot -St0.4c -W1p -Gpurple
cat sample_rate.dat | awk -F ' ' '{if($2==40) print$3,$4}' | gmt plot -St0.4c -W1p -Gfirebrick
gmt legend -DjRB+w5c+o0.2c/0.2c+l1.5 -F+p+gazure1+r << EOF
S 0.5c t 0.4c gold1 0.5p 1.0c sample_rate=100Hz
S 0.5c t 0.4c purple 1.5p 1.0c sample_rate=50Hz
S 0.5c t 0.4c firebrick 0.5p 1.0c sample_rate=40Hz
EOF
gmt colorbar -DJMR+w10c+o0.5c/0c+ml -Bxa1000f -By+l"m"

gmt end show
