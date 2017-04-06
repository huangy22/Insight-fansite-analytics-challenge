#!/usr/bin/env bash

# I'll execute my programs, with the input directory log_input and output the files in the directory log_output
if [ $# -ge 1 ]
then
    if [ "$1" == "--test" -o "$1" == "-t" ];
    then
	mkdir ./log_output/test
	python ./src/process_log.py ./log_input/log_test.txt ./log_output/test/
    elif [ "$1" == "--profile" -o "$1" == "-p" ];
    then
	python -m cProfile -s tottime ./src/process_log.py ./log_input/log.txt ./log_output/
    fi
else
    python ./src/process_log.py ./log_input/log.txt ./log_output/
fi
