# This script requires an ECMWF API-key to operate
# It shall be located in the file $HOME/.ecmwfapirc

#contents of $HOME/.ecmwfapirc (Unix/Linux)
#{
#    "url"   : "https://api.ecmwf.int/v1",
#    "key"   : "XXXXXXXXXXXXXXXXXXXXXX",
#    "email" : "john.smith@example.com"
#}

from datetime import date
from datetime import datetime

from weather.weather import WeatherExtractor, WeatherApi
from ewshopp_area import EwArea

import pandas as pd
import sys

from weather_forecast_2_json import Weather_forecast_2_json

## python main.py  ${work_path_grib}

date_format = '%Y-%m-%d'
start_date_string = str("2019-02-11")
end_date_string = str("2019-02-27")
print "<%s> <%s>" % (start_date_string, end_date_string)

start_date = datetime.strptime(start_date_string.strip(), date_format).date()
end_date = datetime.strptime(end_date_string.strip(), date_format).date()

## Hack for requesting one day
## For a get request the start_date has to be before the end_date. Resulting in minimum two days
## For a fetch request the start_date and end_date can be equal. Resulting in minimum one day
start_get_date = (pd.Timestamp(start_date, freq='D')-1).date()

grib_file = 'milan.grib'
location_coordinates_csv_file = 'milan_locations.csv'
out_result_base = 'milan_fine_grid'

# load forecasted weather data
print 'load grib file'
we = WeatherExtractor()
we.load([grib_file])

print 'get_forecast per entry'
csv = pd.read_csv(location_coordinates_csv_file, header=None)

wf2j = Weather_forecast_2_json(we,
            file_name_combined=out_result_base+'_combined.json')
            
for i in range(len(csv)):
    print 'Location: i %d %s' % (i, csv.loc[i,0])
    wf2j.fetch_forecast(start_date, end_date, csv.loc[i])
            
print 'Ending program'





