
from datetime import date
from datetime import datetime

from weather.weather import WeatherExtractor, WeatherApi
from ewshopp_area import EwArea

import pandas as pd
import sys
import json, collections

from weather_forecast_2_json import Weather_forecast_2_json

## python main.py ${job_json_file} ${region_csv_file} ${work_path_results} 
job_json_file = sys.argv[1]    
region_coordinates_csv_file = sys.argv[2]    
out_result_base = sys.argv[3]

# use OrderedDict to preserve key order in json dicts in python 2.7
with open(job_json_file) as json_file:
    job = json.load(json_file, object_pairs_hook=collections.OrderedDict)
# print json.dumps(job, indent=2, separators=(',', ': ')) # debug printout

forecast_days = int(job.get('forecast_days', 16))
key_map = job.get('key_sequence_map', None)
json_format = job.get('json_format', False)
file_suffix = '_combined.json' if json_format else '_combined.csv'
grib_file = str(job['grib_file'])
print "Grib file:<%s>" % (grib_file)

date_format = '%Y-%m-%d'
start_date_string = str(job['start_date'])
end_date_string = str(job['end_date'])
print "<%s> <%s>" % (start_date_string, end_date_string)

start_date = datetime.strptime(start_date_string.strip(), date_format).date()
end_date = datetime.strptime(end_date_string.strip(), date_format).date()

print "Extracting data from grib file based on Region bounding box coordinates"
print "start_date:%s  end_date:%s" % (start_date.strftime(date_format), end_date.strftime(date_format))
# query the downloaded data

# load forecasted weather data
print 'load grib file'
we = WeatherExtractor()
we.load([grib_file])

print 'get_forecast per entry'
csv = pd.read_csv(region_coordinates_csv_file, header=None)

wf2j = Weather_forecast_2_json(we, json_format, key_map,
            file_name_combined=out_result_base+file_suffix)
            
for i in range(len(csv)):
    print 'Region: i %d %s' % (i, csv.loc[i,1])
    wf2j.fetch_forecast_region(start_date, end_date, csv.loc[i])
            
print 'Ending program'



