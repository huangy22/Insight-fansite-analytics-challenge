#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import read_entry
import datetime as dt

LOGIN_WATCH = {}
LOGIN_BLOCK = {}

LAST_TIME = 0
TIME_LEFT = 1
CHANCE_REMAIN = 2

TIME_WATCH = 20
TIME_BLOCK = 300

def update_block(entry, host, time):
    current = LOGIN_BLOCK[host]
    delta_time = time_difference(current[LAST_TIME], time)
    is_block = False
    if delta_time <= current[TIME_LEFT]:
        is_block = True
        current[LAST_TIME] = time
        current[TIME_LEFT] -= delta_time
    else:
        LOGIN_BLOCK.pop(host, None)
    return is_block


def update_watch(entry, host, time):
    current = LOGIN_WATCH[host]
    delta_time = time_difference(current[LAST_TIME], time)
    if delta_time <= current[TIME_LEFT]:
        if current[CHANCE_REMAIN]==1:
            LOGIN_WATCH.pop(host, None)
            LOGIN_BLOCK[host] = [time, TIME_BLOCK]
        else:
            current[LAST_TIME] = time
            current[TIME_LEFT] -= delta_time
            current[CHANCE_REMAIN] -= 1
    else:
        LOGIN_WATCH.pop(host, None)

def update_log(entry):
    host = entry["Host"]
    time = entry["Time"]
    is_block = False
    if host in LOGIN_BLOCK:
        is_block = update_block(entry, host, time)
    else:
        if entry["Request_Type"]=="POST" and entry["Status"] == 401:
            if host in LOGIN_WATCH:
                update_watch(entry, host, time)
            else:
                LOGIN_WATCH[host] = [time, TIME_WATCH, 2]
        else:
            if host in LOGIN_WATCH:
                LOGIN_WATCH.pop(host, None)
    return is_block

def time_difference(time1, time2):
    return (time2-time1).total_seconds()

class TestLoginErr(unittest.TestCase):
    def setUp(self):
        self.file = "../log_input/log_test.txt"
        #self.file = "../log_input/log.txt"

    def test_time_difference(self):
        time1 = dt.datetime.strptime('01/Jul/1995:00:00:01', "%d/%b/%Y:%H:%M:%S")
        time2 = dt.datetime.strptime('02/Jul/1995:03:00:01', "%d/%b/%Y:%H:%M:%S")
        print time_difference(time1, time2)

    def test_update_watch(self):
        reader = open(self.file, 'r')
        block_file = []
        for line in reader:
            entry = read_entry.read_entry(line)
            is_block = update_log(entry)
            if is_block:
                block_file.append(line)
        print block_file


if __name__ == '__main__':
        unittest.main()

