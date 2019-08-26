import datetime 

from weather.weather import WeatherExtractor, WeatherApi

import sys

def print_data(weather_data):
    for row in weather_data.iterrows():
        # row is tuple (index, columns)
        measure = row[1]
        print "Measurement of %s at from %s for %s" % (measure['shortName'], measure['validDateTime'], measure['validityDateTime'])
        for lat, lon, val in zip(measure['lats'], measure['lons'], measure['values']):
            print "%f N %f S = %f" % (lat, lon, val)






## python main.py ${owm_api} 
owm_api = sys.argv[1]    


wa = WeatherApi(source='owm', key=owm_api)

print 'Requesting owm'

# download forecast data 
wa.get(latlon=(45.364025,9.628995), 
       target='owm_forecast_test.json')

print 'Stored forecast'

# query the downloaded data
we = WeatherExtractor()

# load actual and forecasted weather data
print 'load json file'
we.load(['owm_forecast_test.json'])

points = [{'lat': 45.364025, 'lon': 9.628995}]
weather_data = we.get_forecast(base_date=datetime.date(2019, 8, 26), from_date=datetime.date(2019, 8, 26), to_date=datetime.date(2019, 9, 10))
    
print_data(weather_data)

