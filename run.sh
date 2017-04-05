#!/usr/bin/env bash

# one example of run.sh script for implementing the features using python
# the contents of this script could be replaced with similar files from any major language

# I'll execute my programs, with the input directory log_input and output the files in the directory log_output
python ./src/process_log.py ./log_input/log.txt ./log_output/hosts.txt ./log_output/hours.txt ./log_output/resources.txt ./log_output/blocked.txt ./log_output/hours_no_overlap.txt ./log_output/resources_most_requested.txt ./log_output/resources_least_requested.txt ./log_output/server_error.txt ./log_output/resources_not_found.txt ./log_output/daily_hits.txt ./log_output/daily_users.txt

