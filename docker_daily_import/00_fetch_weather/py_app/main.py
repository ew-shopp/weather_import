# This script requires an ECMWF API-key to operate
# It shall be located in the file $HOME/.ecmwfapirc

#contents of $HOME/.ecmwfapirc (Unix/Linux)
#{
#    "url"   : "https://api.ecmwf.int/v1",
#    "key"   : "XXXXXXXXXXXXXXXXXXXXXX",
#    "email" : "john.smith@example.com"
#}

from datetime import date

from weather.weather import WeatherExtractor, WeatherApi
from ewshopp_area import EwArea

import pandas as pd
import sys

from weather_forecast_2_json import Weather_forecast_2_json

## python main.py ${job_json_file} ${region_csv_file} ${work_path_results} ${work_path_grib}
job_json_file = sys.argv[1]    
region_coordinates_csv_file = sys.argv[2]    
out_result_base = sys.argv[3]
grib_result_base = sys.argv[4]


grib_file = grib_result_base+'.grib'

job = pd.read_json(job_json_file, typ="series")

start_yy = job.loc['start_yy']
start_mm = job.loc['start_mm']              
start_dd = job.loc['start_dd']
end_yy = job.loc['end_yy']
end_mm = job.loc['end_mm'] 
end_dd = job.loc['end_dd']

start_date = date(start_yy, start_mm, start_dd)
end_date = date(end_yy, end_mm, end_dd)

## Hack for requesting one day
## For a get request the start_date has to be before the end_date. Resulting in minimum two days
## For a fetch request the start_date and end_date can be equal. Resulting in minimum one day
start_get_date = (pd.Timestamp(start_date, freq='D')-1).date()

print "grib:%s  region_coordinates:%s out_result_base:%s grib_result_base:%s" % (grib_file, region_coordinates_csv_file, out_result_base, grib_result_base)
print "Get data from ECMWF - start_get_date:%s  end_date:%s" % (start_get_date.strftime('%Y %B %d'), end_date.strftime('%Y %B %d'))

print 'Requesting germay forecast'

wa = WeatherApi()

# download forecast data 
wa.get(from_date=start_get_date, to_date=end_date,
       area=EwArea.Germany, 
       target=grib_file)

print 'Stored forecast'


print "Extracting data from grib file based on Region bounding box coordinates"
print "start_date:%s  end_date:%s" % (start_date.strftime('%Y %B %d'), end_date.strftime('%Y %B %d'))
# query the downloaded data

# load forecasted weather data
print 'load grib file'
we = WeatherExtractor()
we.load([grib_file])

print 'get_forecast per entry'
csv = pd.read_csv(region_coordinates_csv_file, header=None)

wf2j = Weather_forecast_2_json(we,
            file_name_combined=out_result_base+'_combined.json')
            
for i in range(len(csv)):
    print 'Region: i %d %s' % (i, csv.loc[i,1])
    wf2j.fetch_forecast_region(start_date, end_date, csv.loc[i])
            
print 'Ending program'



