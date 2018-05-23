from datetime import date

from weather.weather import WeatherExtractor, WeatherApi

import pandas as pd

from weather_combined import Weather_combined
from weather_separate import Weather_separate

def print_data(weather_data):
    for row in weather_data.iterrows():
        # row is tuple (index, columns)
        measure = row[1]
        print "Measurement of %s at from %s for %s" % (measure['shortName'], measure['validDateTime'], measure['validityDateTime'])
        for lat, lon, val in zip(measure['lats'], measure['lons'], measure['values']):
            print "%f N %f S = %f" % (lat, lon, val)




 
def panda_to_jsonfile(pd, file_name):
    pd.to_json(path_or_buf=file_name, orient='records', date_format='iso', date_unit='s')     
    
def get_forecast_daterange(base_dates, wc, ws, city_elem):

    for bd in base_dates:
        base_date = bd.date()
        base_date_plus_16 = (bd+16).date() # Forecase the next 16 days (probably only 8 present)
        points = [{'lat': city_elem.Latitude, 'lon': city_elem.Longitude}]
        weather_data = we.get_forecast(base_date=base_date, 
            from_date=base_date, to_date=base_date_plus_16, 
            aggtime='hour', aggloc='points',
            interp_points=points)
    
        wc.add_city_weather_data(city_elem.City, weather_data)
        ws.add_city_weather_data(city_elem.City, weather_data)
    
# query the downloaded data
we = WeatherExtractor()

# load actual and forecasted weather data
print 'load grib file'
we.load(['germany_jan2017_dec2017.grib'])


print 'get_forecast per city'
csv = pd.read_csv('german_coordinates.csv')

wc = Weather_combined()
ws = Weather_separate()
#for i in range(len(csv)):
for i in range(3):
    print "City: i %d city %s" % (i, csv.loc[i,"City"])
    #base_dates = pd.date_range(date(2017,1,1), date(2017,1,31))
    base_dates = pd.date_range(date(2017,1,1), date(2017,1,3))

    get_forecast_daterange(base_dates, wc, ws, csv.loc[i])

    
    
print 'Generate the result forecast'
# print_data(weather_data)
panda_to_jsonfile(pd.Series(wc.get_dict_values()), 'germany_cities_forecast_combined.json')
panda_to_jsonfile(pd.Series(ws.get_dict_values()), 'germany_cities_forecast_separate.json')

wc = Weather_combined()
ws = Weather_separate()
for i in range(len(csv)):
    print "i %d city %s" % (i, csv.loc[i,"City"])

    points = [{'lat': csv.loc[i,"Latitude"], 'lon': csv.loc[i,"Longitude"]}]
    weather_data = we.get_actual(from_date=date(
            2017, 1, 1), to_date=date(2017, 12, 31), aggtime='hour', aggloc='points',
            interp_points=points)
            
    wc.add_city_weather_data(csv.loc[i,"City"], weather_data)
    ws.add_city_weather_data(csv.loc[i,"City"], weather_data)
    
print 'Generate the result actual'
# print_data(weather_data)
panda_to_jsonfile(pd.Series(wc.get_dict_values()), 'germany_cities_actual_combined.json')
panda_to_jsonfile(pd.Series(ws.get_dict_values()), 'germany_cities_actual_separate.json')





#print 'get_actual'
#weather_data = we.get_actual(from_date=date(
#    2017, 11, 1), to_date=date(2017, 11, 30), aggtime='hour', aggloc='grid')
#panda = make_panda_combined(weather_data)
#panda_to_jsonfile(panda, 'actual_full1.json')
#panda = make_panda_separate(weather_data)
#panda_to_jsonfile(panda, 'actual_full2.json')



""" Get forecasted data from 1-11-2017 for 2-11-2017, 3-11-2017 and 4-11-2017 for 
two specific points with latitudes and longitudes: (45.01, 13.00) and (46.00, 12.05) """
#points = [{'lat': 45.01, 'lon': 13.0}, {'lat': 46.0, 'lon': 12.05}]
#weather_data = we.get_forecast(base_date=date(2017, 11, 1), from_date=date(
#    2017, 11, 2), to_date=date(2017, 11, 4), aggtime='hour', aggloc='points', interp_points=points)
# print the result
#print_data(weather_data)
#panda = make_panda(weather_data)
#panda_to_jsonfile(panda, 'test2.json')

