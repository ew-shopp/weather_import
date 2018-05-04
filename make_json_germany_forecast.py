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
we.load(['germany_jan2017_dec2017.grib'])


print 'get_forecast per city'
csv = pd.read_csv('german_coordinates.csv')

#wf2j01 = Weather_forecast_2_json(we,
#            'sf/germany_cities_201701_forecast_combined.json',
#            'sf/germany_cities_201701_forecast_separate.json')

wf2j02 = Weather_forecast_2_json(we,
            'sf/germany_cities_201702_forecast_combined.json',
            'sf/germany_cities_201702_forecast_separate.json')

wf2j03 = Weather_forecast_2_json(we,
            'sf/germany_cities_201703_forecast_combined.json',
            'sf/germany_cities_201703_forecast_separate.json')

wf2j04 = Weather_forecast_2_json(we,
            'sf/germany_cities_201704_forecast_combined.json',
            'sf/germany_cities_201704_forecast_separate.json')

wf2j05 = Weather_forecast_2_json(we,
            'sf/germany_cities_201705_forecast_combined.json',
            'sf/germany_cities_201705_forecast_separate.json')

wf2j06 = Weather_forecast_2_json(we,
            'sf/germany_cities_201706_forecast_combined.json',
            'sf/germany_cities_201706_forecast_separate.json')

wf2j07 = Weather_forecast_2_json(we,
            'sf/germany_cities_201707_forecast_combined.json',
            'sf/germany_cities_201707_forecast_separate.json')

wf2j08 = Weather_forecast_2_json(we,
            'sf/germany_cities_201708_forecast_combined.json',
            'sf/germany_cities_201708_forecast_separate.json')

wf2j09 = Weather_forecast_2_json(we,
            'sf/germany_cities_201709_forecast_combined.json',
            'sf/germany_cities_201709_forecast_separate.json')

wf2j10 = Weather_forecast_2_json(we,
            'sf/germany_cities_201710_forecast_combined.json',
            'sf/germany_cities_201710_forecast_separate.json')

wf2j11 = Weather_forecast_2_json(we,
            'sf/germany_cities_201711_forecast_combined.json',
            'sf/germany_cities_201711_forecast_separate.json')

wf2j12 = Weather_forecast_2_json(we,
            'sf/germany_cities_201712_forecast_combined.json',
            'sf/germany_cities_201712_forecast_separate.json')

for i in range(len(csv)):
    print "City: i %d city %s" % (i, csv.loc[i,"City"])
    #wf2j01.fetch_forecast(date(2017,1,1), date(2017,1,31), csv.loc[i])
    wf2j02.fetch_forecast(date(2017,2,1), date(2017,2,28), csv.loc[i])
    wf2j03.fetch_forecast(date(2017,3,1), date(2017,3,31), csv.loc[i])
    wf2j04.fetch_forecast(date(2017,4,1), date(2017,4,30), csv.loc[i])
    wf2j05.fetch_forecast(date(2017,5,1), date(2017,5,31), csv.loc[i])
    wf2j06.fetch_forecast(date(2017,6,1), date(2017,6,30), csv.loc[i])
    wf2j07.fetch_forecast(date(2017,7,1), date(2017,7,31), csv.loc[i])
    wf2j08.fetch_forecast(date(2017,8,1), date(2017,8,31), csv.loc[i])
    wf2j09.fetch_forecast(date(2017,9,1), date(2017,9,30), csv.loc[i])
    wf2j10.fetch_forecast(date(2017,10,1), date(2017,10,31), csv.loc[i])
    wf2j11.fetch_forecast(date(2017,11,1), date(2017,11,30), csv.loc[i])
    wf2j12.fetch_forecast(date(2017,12,1), date(2017,12,31), csv.loc[i])
    
print 'Ending program'


