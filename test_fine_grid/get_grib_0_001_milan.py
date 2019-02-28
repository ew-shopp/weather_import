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

print "Get data from ECMWF - start_get_date:%s  end_date:%s" % (start_get_date.strftime(date_format), end_date.strftime(date_format))

print 'Requesting Milan forecast'

wa = WeatherApi()

# download forecast data 
wa.get(from_date=start_get_date, to_date=end_date,
       area=EwArea.Milan, 
       grid=(0.001, 0.001),
       target=grib_file)

print 'Stored forecast'

print 'Ending program'



