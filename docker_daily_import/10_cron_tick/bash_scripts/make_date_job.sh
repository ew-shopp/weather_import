#!/bin/bash
# arg1: output directory

output_directory=${1}

echo "output_directory: ${output_directory}"
echo '***'

echo '#'
echo '#  Starting: MakeDateJob'
echo '#'

now_timestring=$(date)
echo "Time now: ${now_timestring}"
now_date=$(date +%F)

output_lock_file="${output_directory}/dir_rw.lock"
job_file=${output_directory}/"job_${now_date}.json"

file_content="{\"start_date\": \"${now_date}\", \"end_date\": \"${now_date}\", \"creation_time\": \"${now_timestring}\"}"

# Aquire lock
exec 9>$output_lock_file
echo "// Aquire lock ${output_lock_file}"
if flock 9; then   # Blocking wait
    echo $file_content > $job_file
    chmod 777 $job_file
fi
# Release the lock
exec 9>&-

echo '   Done'

