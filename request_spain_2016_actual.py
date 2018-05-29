from datetime import date

from weather.weather import WeatherExtractor, WeatherApi
from ewshopp_area import EwArea


wa = WeatherApi()

print 'Requesting spain-201601-actual'
# download actual weather data
wa.get(from_date=date(2016, 1, 1), to_date=date(2016, 12, 31),
       area=EwArea.Spain, grid=(0.25, 0.25),
       target='spain-2016-actual.grib', request_type='actual')

print 'Stored spain-201601-actual'




