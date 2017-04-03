#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import read_entry
import algorithms

COUNT_IDX = 0
SIZE_IDX = 1

RESOURCE = {}

def find_large_resources(number, sort_feature):
    if sort_feature=="Count":
        idx = COUNT_IDX 
    elif sort_feature=="Bandwidth":
        idx = SIZE_IDX
    return algorithms.nlargest_dict(number, RESOURCE, idx)

def update_resource(entry):
    """Add the info of entry into the statistics of each resource.
    Args:
        entry(dict): the dictionary of a log info, including keys "Host", "Time",
        "Request", "Reply", "Size".
    Returns:
        None.
    """
    entry_res = entry["Request"]

    if entry_res != "/":
        if entry_res in RESOURCE:
            RESOURCE[entry_res][COUNT_IDX] += 1 
            RESOURCE[entry_res][SIZE_IDX] += entry["Size"]
        else:
            RESOURCE[entry_res] =  [0, 0]
            RESOURCE[entry_res][COUNT_IDX] = 1 
            RESOURCE[entry_res][SIZE_IDX] = entry["Size"]

class TestResource(unittest.TestCase):
    def setUp(self):
        self.file = "../log_input/log_test.txt"
        #['199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 -',
                     #'220.149.67.62 - - [01/Jul/1995:00:00:27 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 200 1204']

    def test_update_resource(self):
        reader = open(self.file, 'r')
        for line in reader:
            entry = read_entry.read_entry(line)
            update_resource(entry)
        #print RESOURCE

    def test_find_large_resources(self):
        reader = open(self.file, 'r')
        for line in reader:
            entry = read_entry.read_entry(line)
            update_resource(entry)
        large_res = find_large_resources(10, "Bandwidth")
        print large_res

if __name__ == '__main__':
        unittest.main()
