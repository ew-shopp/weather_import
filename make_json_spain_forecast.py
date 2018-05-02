from datetime import date

from weather.weather import WeatherExtractor, WeatherApi

import pandas as pd
#from weather_combined import Weather_combined
#from weather_separate import Weather_separate

from weather_forecast_2_json import Weather_forecast_2_json

    
# query the downloaded data

# load forecasted weather data
print 'load grib file'
we = WeatherExtractor()
we.load(['spain_jan2017_dec2017.grib'])


print 'get_forecast per city'
csv = pd.read_csv('spanish_coordinates.csv')

wf2j = Weather_forecast_2_json(we,
            'spain_cities_201701_forecast_combined.json',
            'spain_cities_201701_forecast_separate.json')

for i in range(len(csv)):
    print "City: i %d city %s" % (i, csv.loc[i,"City"])
    wf2j.fetch_forecast(date(2017,1,1), date(2017,1,31), csv.loc[i])
    
print 'Closing flies'
wf2j.close()


