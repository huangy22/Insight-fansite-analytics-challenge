#!/usr/bin/env bash

# one example of run.sh script for implementing the features using python
# the contents of this script could be replaced with similar files from any major language

# I'll execute my programs, with the input directory log_input and output the files in the directory log_output
python ./src/process_log.py ./log_input/log_test.txt ./log_output/hosts_test.txt ./log_output/hours_test.txt ./log_output/resources_test.txt ./log_output/blocked_test.txt ./log_output/hours_no_overlap_test.txt ./log_output/resources_most_requested_test.txt ./log_output/resources_least_requested_test.txt ./log_output/server_error_test.txt ./log_output/resources_not_found_test.txt ./log_output/daily_hits_test.txt ./log_output/daily_users_test.txt

