#!/bin/bash

function gracefulshutdown {
    echo "Main - Received signal ... shutting down"
    exit 0
}

# arg1: retry_max_count
# arg2: code directory
# arg3: input directory
# arg4: work directory
# arg5: output directory
# arg6: cron string

retry_max_count=${1}
code_directory=${2}
input_directory=${3}
work_directory=${4}
output_directory=${5}
cron_string=${6}

#echo "Arguments"
#for i in $*; do 
#   echo "$i" 
#done
#echo "***" 

# Date script to start
job_to_run="${code_directory}/make_date_job.sh"

echo "Main - Starting"

trap gracefulshutdown SIGINT SIGTERM

# Execute init if present
init_script="${code_directory}/init.sh"
if [ -f "$init_script" ]; then
   $init_script
fi

cron_job="${cron_string} /code/make_date_job.sh ${output_directory}"
# cron_job="* * * * * /code/make_date_job.sh /out"
echo "$cron_job" | crontab -
crontab -l
service cron start


echo "Process idle letting cron job do the work ..."
while true; do
    #echo "// Sleeping 60 Seconds"
    sleep 60
done


echo "Main - End"

