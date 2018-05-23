from datetime import date

from weather.weather import WeatherExtractor, WeatherApi

import pandas as pd
import sys

from weather_forecast_2_json import Weather_forecast_2_json

## python main.py ${grib_file} ${work_path} ${work_path_results}
grib_file = sys.argv[1]    
in_csv_file = sys.argv[2]    
out_result_base = sys.argv[3]    
    
print "grib:%s  in:%s result:%s" % (grib_file, in_csv_file, out_result_base)
# query the downloaded data

# load forecasted weather data
print 'load grib file'
we = WeatherExtractor()
we.load([grib_file])

print 'get_forecast per city'
csv = pd.read_csv(in_csv_file, header=None)

wf2j = Weather_forecast_2_json(we,
            out_result_base+'_combined.json',
            out_result_base+'_separate.json')
            
for i in range(len(csv)):
    print 'City: i %d city %s' % (i, csv.loc[i,0])
    wf2j.fetch_forecast(date(2017,1,1), date(2017,12,31), csv.loc[i])
            
print 'Ending program'



