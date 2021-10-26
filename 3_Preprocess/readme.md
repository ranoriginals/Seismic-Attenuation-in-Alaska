### 1. Check arrivals

According to Barcheck et al., (2020), there might be time shift (around 0.05-1s) in the seismic data, we manually check it

### 2. Remove instrument reponse

Based on miniseed and stationxml files, we use obspy to remove the instrument response

### 3. Calculate the spectrum with the multitaper method

### 4. Resample the data and recalculate the spectrum

Since stations used in my research have different sample rate, we want check if we **resample all of them to 100Hz**, what will happen when we re-calculate the spectrum
