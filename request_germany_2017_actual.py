from datetime import date

from weather.weather import WeatherExtractor, WeatherApi
from ewshopp_area import EwArea

wa = WeatherApi()

print 'Requesting germany-2017-actual'


# download actual weather data november 2017
wa.get(from_date=date(2017, 11, 1), to_date=date(2017, 11, 30),
       target='nov2017-actual.grib', request_type='actual')

# download forecast data 
wa.get(from_date=date(2017, 1, 1), to_date=date(2017, 12, 31),
       area=EwArea.Germany, 
       target='germany-2017-actual.grib', request_type='actual')

print 'Stored germany-2017-actual'

