#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Analyze the server log file, get statistics about
hosts, time distribution, resource bandwidth consumption, and block
the user after three failed consecutive login attempts in 20 seconds.
Args:
    input_file(string): The name of the input file
    output_dir(string): The directory where you want to put the output files
Author: Yuan Huang
"""
import os
import sys
import traceback
import read_entry
import host_activity as host
import resource_statistics as resource
import block_hosts
import time_window
import time_statistics
import utility

def output_logs(path, entries, filename, msg):
    """
    Write the selected logs into log file
    Args:
        entries(list): The list contains all the selected logs strings
        filename(string): Name of the output file
        msg(string): Information about the output file
    """
    try:
        log.info(msg)
        with open(os.path.join(path, filename), "w") as writer:
            for entry in entries:
                writer.write(entry)
    except:
        log.info("Fail to output to log file. \n{0}".format(traceback.format_exc()))

def output_statistics(path, records, filename, msg, with_count=True):
    """
    Write the statistics data to output
    Args:
        records(list): The list contains statistical records. Each record is a length-2
            list, with first element the count, and second element as the name of the item
        filename(string): Name of the output file
        msg(string): Information about the output file
        with_count(bool): Whether you want to output both name and count (True) or only
            name(False)
    """
    try:
        log.info(msg)
        with open(os.path.join(path, filename), "w") as writer:
            if with_count:
                for record in records:
                    writer.write(record[1]+","+str(record[0])+"\n")
            else:
                for record in records:
                    writer.write(record[1]+"\n")
    except:
        log.info("Fail to output to file. \n{0}".format(traceback.format_exc()))

# Main Program
infile = sys.argv[1]
outdir = sys.argv[2]

log = utility.Logger("./")

# Initialization for the feature classes
hosts = host.HostActivity()
resources = resource.ResourceStatistics()
time_stat = time_statistics.TimeStatistics()
num_busy_hours = 10
time_window = time_window.TimeWindow(hours=1, n_top=num_busy_hours)
blocked = block_hosts.BlockedHosts(monitor_seconds=20, block_seconds=300, chances=3)

blocked_entries = []
server_errs = []
resources_not_found = set()

log.info("Start to read and process the entries in input file {0}:".format(infile))

try:
    with open(infile, "r") as reader:
        log.info("Reading and processing entry...")

        for entry in reader:
            # Read in each line and transform into a dictionary
            try:
                dict_entry = read_entry.read_entry(entry)
                entry_final = dict_entry
            except TypeError:
                log.warning("Entry format error: {0}{1}"
                            .format(entry, traceback.format_exc()))

            # Update the statistics 
            try:
                hosts.update(dict_entry)
                time_window.update(dict_entry)
                time_stat.update(dict_entry)
                resources.update(dict_entry)

                is_blocked = blocked.update(dict_entry)
                if is_blocked is True:
                    blocked_entries.append(entry)

                if dict_entry["Status"] == 404:
                    resources_not_found.add(dict_entry["Request"]+"\n")

                if dict_entry["Status"] >= 500 and dict_entry["Status"] < 600:
                    server_errs.append(entry)

            except TypeError:
                log.warning("Fail to process entry {0}{1}"
                            .format(entry, traceback.format_exc()))

        # At the end of the file, time window analysis needs extra operations
        # to get final results
        time_window.finalize(entry_final)

        log.info("Reading and processing entries is finished.")

except:
    log.Abort("Fail to process the input file {0} due to reason: \n{1}"
              .format(infile, traceback.format_exc()))

# Feature 1
# Get the top ten active hosts;
# Write the name of hosts and number of activities to output file
num_top_hosts = 10
top_hosts = hosts.top(num_top_hosts, host.COUNT)
output_statistics(outdir, top_hosts, "hosts.txt",
                  "Output the top {0} active hosts to file {1}".format(num_top_hosts, "hosts.txt"))

# Feature 2
# Get the top ten resources consuming the most bandwidth;
# Write the name of resources to output file
num_big_resources = 10
big_resources = resources.top(num_big_resources, resource.BANDWIDTH)
output_statistics(outdir, big_resources, "resources.txt",
                  "Output the top {0} resources that consumes most bandwidth to file {1}"
                  .format(num_big_resources, "resources.txt"), with_count=False)

# Feature 3
# Get the top busiest hours;
# write the top busiest hours and the number of logs to output
top_busy_hours = time_window.top()
output_statistics(outdir, top_busy_hours, "hours.txt",
                  "Output the top {0} busy hours to file {1}"
                  .format(num_busy_hours, "hours.txt"))

# Feature 4
# Write the blocked entries to output
output_logs(outdir, blocked_entries, "blocked.txt", 
            "Output the blocked logs to file {0}".format("blocked.txt"))

# Feature 5
# Get the non-overlapping top busiest hours;
# write the top busiest hours and the number of logs to output
top_busy_hours = time_window.top_no_overlap()
output_statistics(outdir, top_busy_hours, "hours_no_overlap.txt",
                  "Output the top {0} non-overlapping busy hours to file {1}"
                  .format(num_busy_hours, "hours_no_overlap.txt"))

# Feature 6
# Get the top ten resources attracting the most requests;
# Write the name of resources and number of requests to output file
num_most_requested = 10
top_resources = resources.top(num_most_requested, resource.COUNT)
output_statistics(outdir, top_resources, "resources_most_requested.txt",
                  "Output the top {0} resources that users like to request the most {1}"
                  .format(num_most_requested, "resources_most_requested.txt"))

# Feature 7
# Get the ten resources attracting the least requests;
# Write the name of resources and number of requests to output file
num_least_requested = 10
bottom_resources = resources.bottom(num_least_requested, resource.COUNT)
output_statistics(outdir, bottom_resources, "resources_least_requested.txt",
                  "Output the {0} resources that users like to request the least {1}"
                  .format(num_least_requested, "resources_least_requested.txt"))

# Feature 8
# Write the logs with server error to output
output_logs(outdir, server_errs, "server_error.txt",
            "Output the logs with server errors to file {0}".format("server_err.txt"))

# Feature 9
# Write the resources with status 404 (Not Found) to output
output_logs(outdir, resources_not_found, "resources_not_found.txt",
            "Output the resources with status 404 (Not Found) to file {0}"
            .format("resources_not_found.txt"))

# Feature 10
# Write the date and the number of hits on that day to output
daily_hits = time_stat.get_daily_hits()
output_statistics(outdir, daily_hits, "daily_hits.txt",
                  "Output the number of logs on each day to file {0}".format("daily_hits.txt"))

# Feature 11
# Write the date and the number of hosts on that day to output
daily_hosts = time_stat.get_daily_hosts()
output_statistics(outdir, daily_hosts, "daily_hosts.txt",
                  "Output the number of hosts on each day to file {0}".format("daily_hosts.txt"))

# Feature 12

num_sample = 1000
sample_hosts = hosts.sample(num_sample)
output_statistics(outdir, sample_hosts, "hosts_sample.txt",
                  "Output the selected random {0} hosts {1}"
                  .format(num_sample, "hosts_sample.txt"), with_count=False)

# Feature 13
# Number of hits at different time of the day
# Write the hour and the number of hits during that hour to output
hourly_hits = time_stat.get_hourly_hits()
output_statistics(outdir, hourly_hits, "hourly_hits",
                  "Output the number of logs during each hour to file {0}".format("hourly_hits.txt"))

# Feature 14
# Number of hosts at different time of the day
# Write the hour and the number of hosts during that hour to output
hourly_hosts = time_stat.get_hourly_hosts()
output_statistics(outdir, hourly_hosts, "hourly_hosts.txt",
                  "Output the number of hosts during each hour to file {0}".format("hourly_hosts.txt"))

log.info("Memory Usage : {0} MB".format(utility.memory_usage()))
