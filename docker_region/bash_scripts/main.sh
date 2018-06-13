#!/bin/bash
# arg1: tmp file              
# arg2: input directory
# arg3: work directory
# arg4: output directory
# arg5: grib_file
# arg6: start year 
# arg7: start month
# arg8: start date
# arg9: end year
# arg10: end month
# arg11: end date

tmp_file=${1}
input_directory=${2}
work_directory=${3}
output_directory=${4}
grib_file=${5}
start_yy=${6}
start_mm=${7}
start_dd=${8}
end_yy=${9}
end_mm=${10}
end_dd=${11}
 
echo ${tmp_file}
echo ${input_directory}
echo ${work_directory}
echo ${output_directory}
echo ${grib_file}
echo ${start_yy}
echo ${start_mm}
echo ${start_dd}
echo ${end_yy}
echo ${end_mm}
echo ${end_dd}
echo '***'

echo '#'
echo '#   Starting: Main'
echo '#'

wait_count=0
lock_file="${input_directory}/dir_rw.lock"

while [ -f $tmp_file ]; do
    new_file_to_process="no"

    # Aquire lock
    exec 9>$lock_file
    # if flock -n 9; then   # No wait
    echo "// Aquire lock ${lock_file}"
    if flock 9; then
        
        # Check if there are files to process
        nfiles=`find ${input_directory} -name "*.csv" | wc -l`
        if [ "${nfiles}" -gt "0" ]; then
                
            # Extract File Name in random pos
            file_num=`shuf -i1-${nfiles} -n1`
            input_path=`find ${input_directory} -name "*.csv" | head -${file_num} | tail -1`
            echo "// Found ${nfiles} Files"
            echo "// Picking file_num ${file_num}"
            echo "// Processing 1 ${input_path}"

            # Construct Paths
            file_name=${input_path##*/}
            file_name_no_ext=${file_name%.*}
            work_path=${work_directory}/${file_name}
            input_path_renamed=${input_path}.inmove
            work_path_results=${work_directory}/results/${file_name_no_ext}

            # Debug: Show Paths
            echo "!! file_name", ${file_name}
            echo "!! file_name_no_ext", ${file_name_no_ext}
            echo "!! work_path", ${work_path}
            echo "!! work_path_results", ${work_path_results}
            echo "!! output_directory", ${output_directory}
                
            # Check if file already there
            #ls -l ${input_directory}
            #ls -l ${work_directory}
            found_existing=`find ${work_directory} -name ${file_name} | wc -l`
            echo $found_existing
            if [ "${found_existing}" -eq "0" ]; then

                # Move to Workspace
                echo "   Renaming files"
                echo ${input_path}
                echo ${input_path_renamed}
                mv ${input_path} ${input_path_renamed}
                new_file_to_process="yes"

            else
                echo "// File ${file_name} already exists in working dir ... skipping operation"
            fi
        fi
    else
        echo '// Lock failed ... skipping operation'
    fi
    # Release the lock
    exec 9>&-

    if [ $new_file_to_process == "yes" ]; then
        wait_count=0
        # Move renamed file to Workspace
        echo "   Moving to Workspace"
        echo ${input_path_renamed}
        echo ${work_path}
        mv ${input_path_renamed} ${work_path}

        # Files are now in the work dir ... ready to be processed

        # Run the job as a subprocess passing all variables
        source /code/run_job.sh 
    else
        wait_count=$((wait_count+1))
        echo "// Sleeping 60 Seconds $wait_count"
        if [[ $wait_count -gt 10 ]];  then
            echo "Terminating idle script"
            exit 0
        fi
        sleep 60
    fi
done

