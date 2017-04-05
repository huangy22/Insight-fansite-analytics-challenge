#!/usr/bin/env bash

# one example of run.sh script for implementing the features using python
# the contents of this script could be replaced with similar files from any major language

# I'll execute my programs, with the input directory log_input and output the files in the directory log_output
if [ $# -ge 1 ]
then
    if [ "$1" == "--test" -o "$1" == "-t" ];
    then
	python ./src/process_log.py ./log_input/log_test.txt ./log_output/test/
    elif [ "$1" == "--profile" -o "$1" == "-p" ];
    then
	python -m cProfile -s tottime ./src/process_log.py ./log_input/log.txt ./log_output/
    fi
else
    python ./src/process_log.py ./log_input/log.txt ./log_output/
fi

