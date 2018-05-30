#!/bin/bash

echo '#'
echo '#  Starting Job: Location grib weather extraction'
echo '#'
# Debug: Show Paths
echo "!! work_path", ${work_path}
echo "!! file_name", ${file_name}
echo "!! work_path_results", ${work_path_results}

# TODO Where shall these come from
echo "!! grib_file", ${grib_file}


# Files are now in the work dir ... ready to be processed

# Make imported dir if not there
mkdir -p ${work_directory}/results

# Uploading
echo "   Starting python script"
cd /weather/weather-data-master/weather_import
echo "Running:  python main.py ${grib_file} ${work_path} ${work_path_results} ${start_yy} ${start_mm} ${start_dd} ${end_yy} ${end_mm} ${end_dd}"
python main.py ${grib_file} ${work_path} ${work_path_results} ${start_yy} ${start_mm} ${start_dd} ${end_yy} ${end_mm} ${end_dd}


# Run move_to_output as a subprocess passing all variables
# TODO source /code/move_to_output.sh

echo '   Done'

