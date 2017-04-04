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
import host_activity
import resource_statistics
import block_hosts
import time_statistics
import utility

infile = sys.argv[1]
outfiles = {}
outfiles["hosts"] = sys.argv[2]
outfiles["hours"] = sys.argv[3]
outfiles["resources"] = sys.argv[4]
outfiles["blocked"] = sys.argv[5]

log = utility.Logger("./")

hosts = host_activity.HostActivity()
resources = resource_statistics.ResourceStatistics()
hours = time_statistics.TimeStatistics(hours=1, n_top=10)
blocked = block_hosts.BlockedHosts(watch_seconds=20, block_seconds=300, chances=3)

blocked_entries = []

log.info("Start to read and process the entries in input file {0}:".format(infile))

try:
    with open(infile, "r") as reader:
        log.info("Reading and processing entry...")

        for entry in reader:
            try:
                dict_entry = read_entry.read_entry(entry)

                hosts.update(dict_entry)
                hours.update(dict_entry)

                is_blocked = blocked.update(dict_entry)
                if is_blocked is True:
                    blocked_entries.append(entry)

                if dict_entry["Request_Type"] == "GET":
                    resources.update(dict_entry)
            except TypeError:
                log.info("Fail to process entry {0}{1}".
                         format(entry, traceback.format_exc()))

        log.info("Reading and processing entries is finished.")

except IOError:
    log.Abort("Fail to open the input file {0} due to {1}"
                 .format(infile, traceback.format_exc()))


try:
    log.info("Output the blocked host activities to file {0}".format(outfiles["blocked"]))

    with open(outfiles["blocked"], "w") as writer:
        for entry in blocked_entries:
            writer.write(entry)

except IOError:
    log.info("Fail to output the blocked host activitites. \n{0}".format(traceback.format_exc()))

try:
    log.info("Output the top ten busy hours to file {0}".format(outfiles["hours"]))

    top_busy_hours = hours.top()
    with open(outfiles["hours"], "w") as writer:
        for record in top_busy_hours:
            writer.write(record[1]+", "+str(record[0])+"\n")

except IOError:
    log.info("Fail to output the top ten busy hours. \n{0}".
             format(traceback.format_exc()))

try:
    log.info("Output the top ten active hosts to file {0}".format(outfiles["hosts"]))

    top_hosts = hosts.top(10, hosts.count)
    with open(outfiles["hosts"], "w") as writer:
        for record in top_hosts:
            writer.write(record[1]+", "+str(record[0])+"\n")

except NotImplementedError:
    log.info("Fail to obtain the top active hosts because the sort feature not implemented.\
             \n{0}".format(traceback.format_exc()))

except IOError:
    log.info("Fail to output the top ten active hosts. \n{0}".
             format(traceback.format_exc()))

try:

    log.info("Output the top ten resources that consumes most bandwidth to file {0}".
             format(outfiles["resources"]))
    top_resources = resources.top(10, resources.bandwidth)

    with open(outfiles["resources"], "w") as writer:
        for record in top_resources:
            writer.write(record[1]+"\n")

except NotImplementedError:
    log.info("Fail to obtain the top resources because the sort feature is not implemented.\
             \n{0}".format(traceback.format_exc()))

except IOError:
    log.info("Fail to output the top ten resources. \n{0}".
             format(traceback.format_exc()))

log.info("Memory Usage : {0} MB".format(utility.memory_usage()))
