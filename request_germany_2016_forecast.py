from datetime import date

from weather.weather import WeatherExtractor, WeatherApi
from ewshopp_area import EwArea

wa = WeatherApi()

print 'Requesting germay-2016-forecast'

# download forecast data 
wa.get(from_date=date(2016, 1, 1), to_date=date(2016, 12, 31),
       area=EwArea.Germany, 
       target='germay_jan2016_dec2016.grib')

print 'Stored germany-2016-forecast'

