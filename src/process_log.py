"""The main code to process the server log file and get statistics.
"""
import sys
import read_entry
import host_activity
import resource_statistics
import block_hosts
import time_statistics
from logger import *

if __name__ == "__main__":

    INFILE = sys.argv[1]
    OUTFILES = {}
    OUTFILES["hosts"] = sys.argv[2]
    OUTFILES["hours"] = sys.argv[3]
    OUTFILES["resources"] = sys.argv[4]
    OUTFILES["blocked"] = sys.argv[5]

    hosts = host_activity.HostActivity()
    resources = resource_statistics.ResourceStatistics()
    hours = time_statistics.TimeStatistics(hours=1, n_top=10)
    blocked = block_hosts.BlockedHosts(watch_seconds=20, block_seconds=300, chances=3)

    blocked_logs = []

    log.info("Start to read in the input file {0}:".format(INFILE))
    with open(INFILE, "r") as reader:
        for entry in reader:
            #try:
            dict_entry = read_entry.read_entry(entry)

            hosts.update(dict_entry)
            hours.update(dict_entry)

            is_blocked = blocked.update(dict_entry)
            if is_blocked is True:
                blocked_logs.append(entry)

            if dict_entry["Request_Type"] == "GET":
                resources.update(dict_entry)
            #except:
                #log.info()
    #except:

    with open(OUTFILES["blocked"], "w") as writer:
        for log in blocked_logs:
            writer.write(log)

    top_busy_hours = hours.top()
    with open(OUTFILES["hours"], "w") as writer:
        for record in top_busy_hours:
            writer.write(record[1]+", "+str(record[0])+"\n")

    top_hosts = hosts.top(10, hosts.count)
    with open(OUTFILES["hosts"], "w") as writer:
        for record in top_hosts:
            writer.write(record[1]+", "+str(record[0])+"\n")

    top_resources = resources.top(10, resources.bandwidth)
    with open(OUTFILES["resources"], "w") as writer:
        for record in top_resources:
            writer.write(record[1]+"\n")
