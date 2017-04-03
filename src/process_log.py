#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
The main code to analyze the server log file and get statistics about 
hosts, time distribution, resource bandwidth consumption and so on.
Author: Yuan Huang
"""
import sys
import traceback
import read_entry
import host_activity
import resource_statistics
import block_hosts
import time_statistics
import logger

infile = sys.argv[1]
outfiles = {}
outfiles["hosts"] = sys.argv[2]
outfiles["hours"] = sys.argv[3]
outfiles["resources"] = sys.argv[4]
outfiles["blocked"] = sys.argv[5]

log = logger.log

hosts = host_activity.HostActivity()
resources = resource_statistics.ResourceStatistics()
hours = time_statistics.TimeStatistics(hours=1, n_top=10)
blocked = block_hosts.BlockedHosts(watch_seconds=20, block_seconds=300, chances=3)

blocked_entries = []

log.info("Start to read and process the entries in input file %s:", infile)

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
                log.info("Fail to process entry %s%s",
                         entry, traceback.format_exc())

        log.info("Reading and processing entries is finished.")

except IOError:
    logger.Abort("Fail to open the input file {0} due to {1}"
                 .format(infile, traceback.format_exc()))


try:
    log.info("Output the blocked host activities to file %s", outfiles["blocked"])

    with open(outfiles["blocked"], "w") as writer:
        for entry in blocked_entries:
            writer.write(entry)

except IOError:
    log.info("Fail to output the blocked host activitites. \n%s", traceback.format_exc())

try:
    log.info("Output the top ten busy hours to file %s", outfiles["hours"])

    top_busy_hours = hours.top()
    with open(outfiles["hours"], "w") as writer:
        for record in top_busy_hours:
            writer.write(record[1]+", "+str(record[0])+"\n")

except IOError:
    log.info("Fail to output the top ten busy hours. \n%s",
             traceback.format_exc())

try:
    log.info("Output the top ten active hosts to file %s", outfiles["hosts"])

    top_hosts = hosts.top(10, hosts.count)
    with open(outfiles["hosts"], "w") as writer:
        for record in top_hosts:
            writer.write(record[1]+", "+str(record[0])+"\n")

except NotImplementedError:
    log.info("Fail to obtain the top active hosts because the sort feature not implemented.\
             \n%s", traceback.format_exc())

except IOError:
    log.info("Fail to output the top ten active hosts. \n%s",
             traceback.format_exc())

try:

    log.info("Output the top ten resources that consumes most bandwidth to file %s",
             outfiles["resources"])
    top_resources = resources.top(10, resources.bandwidth)

    with open(outfiles["resources"], "w") as writer:
        for record in top_resources:
            writer.write(record[1]+"\n")

except NotImplementedError:
    log.info("Fail to obtain the top resources because the sort feature is not implemented.\
             \n%s", traceback.format_exc())

except IOError:
    log.info("Fail to output the top ten resources. \n%s",
             traceback.format_exc())
