from datetime import date

from weather.weather import WeatherExtractor, WeatherApi
from ewshopp_area import EwArea

wa = WeatherApi()

print 'Requesting spain-201601-forecast'

# download forecast data 
wa.get(from_date=date(2016, 1, 1), to_date=date(2016, 1, 31),
       area=EwArea.Spain, grid=(0.25, 0.25),
       target='spain-201601-test-forecast.grib', request_type='forecast')

print 'Stored spain-201601-forecast'

