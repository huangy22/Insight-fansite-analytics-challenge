import sys
import read_entry
import host_activity
import resource_statistics
import block_hosts
import time_statistics
#import logger

if __name__ == "__main__":

    infile = sys.argv[1]
    outfiles = {}
    outfiles["hosts"] = sys.argv[2]
    outfiles["hours"] = sys.argv[3]
    outfiles["resources"] = sys.argv[4]
    outfiles["blocked"] = sys.argv[5]

    hosts = host_activity.HostActivity()
    resources = resource_statistics.ResourceStatistics()
    hours = time_statistics.TimeStatistics(hours=1, n_top=10)
    blocked = block_hosts.BlockedHosts(watch_seconds=20, block_seconds=300, chances=3) 

    blocked_logs = []

    with open(infile, "r") as reader:
        for entry in reader:
            #try:
            dict_entry = read_entry.read_entry(entry)

            hosts.update(dict_entry)
            hours.update(dict_entry)

            is_blocked = blocked.update(dict_entry)
            if is_blocked is True:
                blocked_logs.append(entry)

            if dict_entry["Request_Type"]=="GET":
                resources.update(dict_entry)
            #except:
                #log.info()
    #except:

    with open(outfiles["blocked"], "w") as writer:
        for i in range(len(blocked_logs)):
            writer.write(blocked_logs[i])

    top_busy_hours = hours.top()
    with open(outfiles["hours"], "w") as writer:
        for i in range(len(top_busy_hours)):
            writer.write(top_busy_hours[i][1]+", "+str(top_busy_hours[i][0])+"\n")

    top_hosts, top_number = hosts.top(10, hosts.COUNT)
    with open(outfiles["hosts"], "w") as writer:
        for i in range(len(top_hosts)):
            writer.write(top_hosts[i]+", "+str(top_number[i])+"\n")

    top_resources, top_bandwidth = resources.top(10,  resources.BANDWIDTH)
    with open(outfiles["resources"], "w") as writer:
        for i in range(len(top_resources)):
            writer.write(top_resources[i]+"\n")

