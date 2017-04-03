import read_entry
import active_host
import large_resource
import log_err_block
import busiest_time

if __name__ == "__main__":
    block_logs = []

    #with open("../log_input/log_test2.txt", "r") as reader:
    with open("../log_input/log.txt", "r") as reader:
        for entry in reader:
            dict_entry = read_entry.read_entry(entry)
            
            active_host.update_host(dict_entry)
            busiest_time.update_time(dict_entry)
            block = log_err_block.update_log(dict_entry)
            if block:
                block_logs.append(entry)

            if dict_entry["Request_Type"]=="GET":
                large_resource.update_resource(dict_entry)

    #print block_logs
    #with open("../log_output/blocked_test.txt", "w") as writer:
    with open("../log_output/blocked.txt", "w") as writer:
        for i in range(len(block_logs)):
            writer.write(block_logs[i])

    top_busy_hours = busiest_time.find_busiest_periods()
    #with open("../log_output/hours_test.txt", "w") as writer:
    with open("../log_output/hours.txt", "w") as writer:
        for i in range(len(top_busy_hours)):
            writer.write(top_busy_hours[i][1]+", "+str(top_busy_hours[i][0])+"\n")

    top_hosts, top_number = active_host.find_active_hosts(10, "Count")
    #print top_hosts, top_number
    with open("../log_output/hosts.txt", "w") as writer:
    #with open("../log_output/hosts_test.txt", "w") as writer:
        for i in range(len(top_hosts)):
            writer.write(top_hosts[i]+", "+str(top_number[i])+"\n")

    top_resources, top_bandwidth = large_resource.find_large_resources(10, "Bandwidth")
    #print top_resources
    #with open("../log_output/resources_test.txt", "w") as writer:
    with open("../log_output/resources.txt", "w") as writer:
        for i in range(len(top_resources)):
            writer.write(top_resources[i]+"\n")

