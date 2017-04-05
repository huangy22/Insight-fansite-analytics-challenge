#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Analyze the server log file, get statistics about
hosts, time distribution, resource bandwidth consumption, and block
the user after three failed consecutive login attempts in 20 seconds.
Author: Yuan Huang
"""
import sys
import traceback
import read_entry
import host_activity as host
import resource_statistics as resource
import block_hosts
import time_statistics
import utility

def output_logs(entries, filename, msg):
    # Write the selected logs into log file
    try:
        log.info(msg)
        with open(filename, "w") as writer:
            for entry in entries:
                writer.write(entry)
    except:
        log.info("Fail to output to log file. \n{0}".format(traceback.format_exc()))

def output_statistics(records, filename, msg, with_count=True):
    # Write the statistics data to output
    try:
        log.info(msg)
        with open(filename, "w") as writer:
            if with_count:
                for record in records:
                    writer.write(record[1]+","+str(record[0])+"\n")
            else:
                for record in records:
                    writer.write(record[1]+"\n")
    except:
        log.info("Fail to output to file. \n{0}".format(traceback.format_exc()))

infile = sys.argv[1]
outfiles = {}
outfiles["hosts"] = sys.argv[2]
outfiles["hours"] = sys.argv[3]
outfiles["resources"] = sys.argv[4]
outfiles["blocked"] = sys.argv[5]
outfiles["hours_no_overlap"] = sys.argv[6]
outfiles["resources_most_requested"] = sys.argv[7]
outfiles["resources_least_requested"] = sys.argv[8]
outfiles["server_err"] = sys.argv[9]
outfiles["resources_not_found"] = sys.argv[10]
outfiles["daily_hits"] = sys.argv[11]
outfiles["daily_users"] = sys.argv[12]

log = utility.Logger("./")

hosts = host.HostActivity()
resources = resource.ResourceStatistics()
time = time_statistics.TimeStatistics(hours=1, n_top=10)
blocked = block_hosts.BlockedHosts(watch_seconds=20, block_seconds=300, chances=3)

blocked_entries = []
server_errs = []
resources_not_found = set()

log.info("Start to read and process the entries in input file {0}:".format(infile))

try:
    with open(infile, "r") as reader:
        log.info("Reading and processing entry...")

        for entry in reader:
            try:
                dict_entry = read_entry.read_entry(entry)
                entry_final = dict_entry
            except TypeError:
                log.warning("Entry format error: {0}{1}"
                            .format(entry, traceback.format_exc()))
            try:
                hosts.update(dict_entry)
                time.update(dict_entry)
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
        time.finalize(entry_final)

        log.info("Reading and processing entries is finished.")

except:
    log.Abort("Fail to process the input file {0} due to reason: \n{1}"
              .format(infile, traceback.format_exc()))

# Feature 1
# Get the top ten active hosts;
# Write the name of hosts and number of activities to output file
top_hosts = hosts.top(10, host.COUNT)
output_statistics(top_hosts, outfiles["hosts"],
                  "Output the top ten active hosts to file {0}".format(outfiles["hosts"]))

# Feature 2
# Get the top ten resources consuming the most bandwidth;
# Write the name of resources to output file
big_resources = resources.top(10, resource.BANDWIDTH)
output_statistics(big_resources, outfiles["resources"],
                  "Output the top ten resources that consumes most bandwidth to file {0}"
                  .format(outfiles["resources"]), with_count=False)

# Feature 3
# Get the top busiest hours;
# write the top busiest hours and the number of logs to output
top_busy_hours = time.top()
output_statistics(top_busy_hours, outfiles["hours"],
                  "Output the top ten busy hours to file {0}".format(outfiles["hours"]))

# Feature 4
# Write the blocked entries to output
output_logs(blocked_entries, outfiles["blocked"], 
            "Output the blocked logs to file {0}".format(outfiles["blocked"]))

# Feature 5
# Get the non-overlapping top busiest hours;
# write the top busiest hours and the number of logs to output
top_busy_hours = time.top_no_overlap()
output_statistics(top_busy_hours, outfiles["hours_no_overlap"],
                  "Output the top ten non-overlapping busy hours to file {0}"
                  .format(outfiles["hours_no_overlap"]))

# Feature 6
# Get the top ten resources attracting the most requests;
# Write the name of resources and number of requests to output file
top_resources = resources.top(10, resource.COUNT)
output_statistics(top_resources, outfiles["resources_most_requested"],
                  "Output the top ten resources that users like to request the most {0}"
                  .format(outfiles["resources_most_requested"]))

# Feature 7
# Get the ten resources attracting the least requests;
# Write the name of resources and number of requests to output file
bottom_resources = resources.bottom(10, resource.COUNT)
output_statistics(bottom_resources, outfiles["resources_least_requested"],
                  "Output the ten resources that users like to request the least {0}"
                  .format(outfiles["resources_least_requested"]))

# Feature 8
# Write the logs with server error to output
output_logs(server_errs, outfiles["server_err"],
            "Output the logs with server errors to file {0}".format(outfiles["server_err"]))

# Feature 9
# Write the resources with status 404 (Not Found) to output
output_logs(resources_not_found, outfiles["resources_not_found"],
            "Output the resources with status 404 (Not Found) to file {0}"
            .format(outfiles["resources_not_found"]))

# Feature 10
daily_hits = time.get_daily_hits()
output_statistics(daily_hits, outfiles["daily_hits"],
                  "Output the number of logs on each day to file {0}".format(outfiles["daily_hits"]))

# Feature 11
daily_users = time.get_daily_users()
output_statistics(daily_users, outfiles["daily_users"],
                  "Output the number of users on each day to file {0}".format(outfiles["daily_users"]))


log.info("Memory Usage : {0} MB".format(utility.memory_usage()))