### Download the AACSE Earthquake Catalog

May. - Dec. 2018: https://scholarworks.alaska.edu/handle/11122/11418

Jan. - Aug. 2019: https://scholarworks.alaska.edu/handle/11122/11967 

(There are some problems in July 2019 catalog, waiting for update)

### In the original catalog files (QuakeML format), a few events have times like yyyy-mm-ddT**:**:60.000Z, which is not supported by ObsPy.

`find *.quakeml | xargs grep -ri ":60.000Z"`
- XO_2018_06.quakeml: 2018-06-18T21:56:60.000Z ➔ 2018-06-18T21:57:00.000Z
- XO_2018_10.quakeml: 2020-11-19T01:12:60.000Z ➔ 2020-11-19T01:13:00.000Z
- XO_2018_11.quakeml: 2018-11-14T00:42:60.000Z ➔ 2018-11-14T00:43:00.000Z
- XO_2019_02.quakeml: 2021-02-09T02:50:60.000Z ➔ 2021-02-09T02:51:00.000Z
- XO_2019_04.quakeml: 2021-05-11T20:56:60.000Z ➔ 2021-05-11T20:57:00.000Z

### AACSE Earthquake Catalog

Time range: 2018-05-12 ⇒ 2019-08-24

Numbers of Events: 7242

Number of Events with depth over 50km: 1969

### Picks

Number of picks: 433104

Number of P wave picks: 303602

Number of S wave picks: 129502
