#!/usr/bin/env bash
# Execute the programs, with the input directory log_input and output the files in the directory log_output
python -m cProfile -s tottime ./src/process_log.py ./log_input/log.txt ./log_output/

