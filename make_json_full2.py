from datetime import date

from weather.weather import WeatherExtractor, WeatherApi

import pandas as pd
import numpy as np

def print_data(weather_data):
    for row in weather_data.iterrows():
        # row is tuple (index, columns)
        measure = row[1]
        print "Measurement of %s at from %s for %s" % (measure['shortName'], measure['validDateTime'], measure['validityDateTime'])
        for lat, lon, val in zip(measure['lats'], measure['lons'], measure['values']):
            print "%f N %f S = %f" % (lat, lon, val)

def increment_element(d, field):
    if field not in d:
        d[field] = 1
    else:
        d[field] = d[field] + 1
        
def make_panda(weather_data):
    d = {}
    masked_with_nan = {}
    for row in weather_data.iterrows():
        # row is tuple (index, columns)
        measure = row[1]
        # print "Measurement of %s at from %s for %s" % (measure['shortName'], measure['validDateTime'], measure['validityDateTime'])
        for lat, lon, val in zip(measure['lats'], measure['lons'], measure['values']):
            # print "%f N %f S = %f" % (lat, lon, val)
            common = "%f,%f,%s,%s,%s" % (lat, lon, measure['validDateTime'], measure['validityDateTime'], measure['shortName'])
            if common not in d:
                d[common] = {}
            d[common]['position'] = [lat, lon]
            d[common]['validTime'] = measure['validDateTime']
            d[common]['validityDateTime'] = measure['validityDateTime']
            d[common]['valueName'] = measure['shortName']
            if type(val) == np.ma.core.MaskedConstant:
                d[common][measure['shortName']+'masked'] = True
                d[common][measure['shortName']] = np.nan
                d[common]['value'] = np.nan
                increment_element(masked_with_nan, measure['shortName'])
            else:
                d[common][measure['shortName']] = val
                d[common]['value'] = val
                
    for key in masked_with_nan:
        print "Replacing masked element '%s' with NaN %d times" % (key, masked_with_nan[key])
    return pd.Series(d.values())

def check_array(array):
    for idx in range(len(array)):
        print idx
        j = pd.Series(array[idx]).to_json()

def panda_to_jsonfile(pd, file_name):
    pd.to_json(path_or_buf=file_name, orient='records', date_format='iso', date_unit='s')        
    
# query the downloaded data
we = WeatherExtractor()
# load actual and forecasted weather data
we.load(['nov2017-forecast.grib', 'nov2017-actual.grib'])

print 'get_forecast'
weather_data = we.get_forecast(base_date=date(2017, 11, 1), from_date=date(
    2017, 11, 1), to_date=date(2017, 11, 30), aggtime='hour', aggloc='grid')

# print the result
# print_data(weather_data)

panda = make_panda(weather_data)
panda_to_jsonfile(panda, 'forecast_full2.json')

print 'get_actual'
weather_data = we.get_actual(from_date=date(
    2017, 11, 1), to_date=date(2017, 11, 30), aggtime='hour', aggloc='grid')
panda = make_panda(weather_data)
panda_to_jsonfile(panda, 'actual_full2.json')


""" Get forecasted data from 1-11-2017 for 2-11-2017, 3-11-2017 and 4-11-2017 for 
two specific points with latitudes and longitudes: (45.01, 13.00) and (46.00, 12.05) """
#points = [{'lat': 45.01, 'lon': 13.0}, {'lat': 46.0, 'lon': 12.05}]
#weather_data = we.get_forecast(base_date=date(2017, 11, 1), from_date=date(
#    2017, 11, 2), to_date=date(2017, 11, 4), aggtime='hour', aggloc='points', interp_points=points)
# print the result
#print_data(weather_data)
#panda = make_panda(weather_data)
#panda_to_jsonfile(panda, 'test2.json')

