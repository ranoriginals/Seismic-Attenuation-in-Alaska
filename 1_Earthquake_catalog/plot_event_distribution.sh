#!/bin/bash
# plot the distributions of stations (detailed version)

region="-165/-145/51/61"
projection="M16c"

gmt begin station_info pdf A+m0.5c
gmt basemap -R$region -J$projection -Ba2 -BWSen 
gmt grdimage -R$region -J$projection @earth_relief_01m -I+d
awk -F ' ' '{print $3,$4}' stainfo.dat | gmt plot -St0.3c -W1p -GGOLD1 
gmt plot -A -W2p,white,- << EOF
-163 51
-147 51
-147 60
-163 60
-163 51
EOF
echo -162.8 58 May-Dec,2018 | gmt text -F+f15p,7
echo -163 57.5 3829 events | gmt text -F+f15p,7
echo -163 57 190 stations | gmt text -F+f15p,7
awk -F ' ' '{print $2,$3}' AACSE_catalog_2018.dat | gmt plot -Sc0.2c -W0.5p,red
gmt colorbar -DJMR+w10c+o0.5c/0c+ml -Bxa1000f -By+l"m"

gmt end show
