#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import read_entry
import algorithms
import datetime as dt
from collections import deque

TIME_WINDOW = dt.timedelta(minutes=1)

N_TOP = 10

COUNT_IDX = 0
TIME_IDX = 1

time_queue = deque()
time_queue.append(dt.datetime.min)

top_list = algorithms.LinkedList(N_TOP)
last_node = algorithms.Node([0, dt.datetime.min])
top_list.sorted_insert_node(last_node)
last_sorted = True

def update_current_window(entry):
    global time_queue
    time = entry["Time"]
    if time > time_queue[-1]:
        time_queue.append(time)
        while time_queue[0] <= time_queue[-1]-TIME_WINDOW:
            time_queue.popleft()
    else:
        time_queue.append(time)
    return len(time_queue), time_queue[-1]

def update_top_list(n, time):
    global last_node
    global top_list
    global last_sorted

    if time-TIME_WINDOW < last_node.data[TIME_IDX]:
        if n > last_node.data[COUNT_IDX]:
            top_list.replace_data(last_node, [n, time])
            last_sorted = False
    else: 
        if not last_sorted:
            last_node = top_list.sort_node(last_node)
            last_sorted = True
        if top_list.length < top_list.max_length or n > top_list.min()[0]:
            last_node = top_list.sorted_insert_data([n, time])
        if top_list.length < top_list.max_length or n > top_list.min()[0]:
            last_node = top_list.sorted_insert_data([n, time])

def update_time(entry):
    n, time = update_current_window(entry)
    update_top_list(n, time)

def find_busiest_periods():
    result = top_list.get_list()
    for data in result:
        data[1] = (data[1]-TIME_WINDOW).strftime("%d/%b/%Y:%H:%M:%S"+ " -0400")
    return result

class TestLoginErr(unittest.TestCase):
    def setUp(self):
        self.file = "../log_input/log_test.txt"
        #self.file = "../log_input/log.txt"

    def test_update_top_list(self):
        reader = open(self.file, 'r')
        for line in reader:
            entry = read_entry.read_entry(line)
            n, time = update_current_window(entry)
            update_top_list(n, time)
        result = top_list.get_list()
        for data in result:
            data[1] = (data[1]-TIME_WINDOW).strftime("%d/%b/%Y:%H:%M:%S -0400")
        print result

if __name__ == '__main__':
        unittest.main()


