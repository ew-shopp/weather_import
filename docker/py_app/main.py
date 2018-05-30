from datetime import date

from weather.weather import WeatherExtractor, WeatherApi

import pandas as pd
import sys

from weather_forecast_2_json import Weather_forecast_2_json

## python main.py ${grib_file} ${work_path} ${work_path_results}
grib_file = sys.argv[1]    
in_csv_file = sys.argv[2]    
out_result_base = sys.argv[3]
start_yy = int(sys.argv[4])
start_mm = int(sys.argv[5])               
start_dd = int(sys.argv[6])
end_yy = int(sys.argv[7])
end_mm = int(sys.argv[8])  
end_dd = int(sys.argv[9])

start_date = date(start_yy, start_mm, start_dd)
end_date = date(end_yy, end_mm, end_dd)
    
print "grib:%s  in:%s result:%s" % (grib_file, in_csv_file, out_result_base)
print "start_date:%s  end_date:%s" % (start_date.strftime('%Y %B %d'), end_date.strftime('%Y %B %d'))
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
    wf2j.fetch_forecast(start_date, end_date, csv.loc[i])
            
print 'Ending program'



