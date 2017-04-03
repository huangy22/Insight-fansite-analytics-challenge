#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import read_entry
import algorithms 

COUNT_IDX = 0
SIZE_IDX = 1

HOST= {}

def update_host(entry):
    """Add the info of entry into the statistics of each host.
    Args:
        entry(dict): the dictionary of a log info, including keys "Host", "Time",
        "Request", "Reply", "Size".
    Returns:
        None.
    """
    if entry["Host"] in HOST:
        HOST[entry["Host"]][COUNT_IDX] += 1 
        HOST[entry["Host"]][SIZE_IDX] += entry["Size"]
    else:
        HOST[entry["Host"]] = [0, 0] 
        HOST[entry["Host"]][COUNT_IDX] = 1 
        HOST[entry["Host"]][SIZE_IDX] = entry["Size"]

def find_active_hosts(number, sort_feature):
    top = []
    if sort_feature=="Count":
        idx = COUNT_IDX 
    elif sort_feature=="Size":
        idx = SIZE_IDX
    return algorithms.nlargest_dict(number, HOST, idx)

class TestHost(unittest.TestCase):
    def setUp(self):
        #self.file = ['199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 -',
                     #'220.149.67.62 - - [01/Jul/1995:00:00:27 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 200 1204']
        self.file = "../log_input/log_test.txt"

    def test_update_host(self):
        reader = open(self.file, 'r')
        block_file = []
        for line in reader:
            entry = read_entry.read_entry(line)
            update_host(entry)
        #print HOST

    def test_find_active_hosts(self):
        reader = open(self.file, 'r')
        block_file = []
        for line in reader:
            entry = read_entry.read_entry(line)
            update_host(entry)
        active_hosts = find_active_hosts(10, "Count")
        print active_hosts

if __name__ == '__main__':
        unittest.main()
