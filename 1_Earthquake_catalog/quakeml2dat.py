from obspy import read_events
# read quakemlfiles and extract event information

cat = read_events("*.quakeml")
with open("AACSE_catalog.dat", "w") as fcat:
    for event in cat:
        origin = event.origins[0]
        magnitude = event.magnitudes[0]
        fcat.write(
            "{} {:9.4f} {:8.4f} {:5.1f} {:3.1f} {}\n".format(
                origin.time,
                origin.longitude,
                origin.latitude,
                origin.depth / 1000.0,
                magnitude.mag,
                event.resource_id.id.split("/")[2],
            )
        )
