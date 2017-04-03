#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import read_entry
import datetime as dt

class BlockedHosts(object):
    def __init__(self, watch_seconds=20, block_seconds=300, chances=3):
        self.watch_time = watch_seconds
        self.block_time = block_seconds
        self.chances = chances

        self.__watch = {}
        self.__block = {}

        self.__last_post_index = 0
        self.__time_left_index = 1
        self.__chances_left_index = 2

    def __update_block(self, entry, host, time):
        status = self.__block[host]
        delta_time = time_difference(status[self.__last_post_index], time)
        is_blocked = False
        if delta_time <= status[self.__time_left_index]:
            is_blocked = True
            status[self.__last_post_index] = time
            status[self.__time_left_index] -= delta_time
        else:
            self.__block.pop(host, None)
        return is_blocked


    def __update_watch(self, entry, host, time):
        status = self.__watch[host]
        delta_time = time_difference(status[self.__last_post_index], time)
        if delta_time <= status[self.__time_left_index]:
            if status[self.__chances_left_index]==1:
                self.__watch.pop(host, None)
                self.__block[host] = [time, self.block_time]
            else:
                status[self.__last_post_index] = time
                status[self.__time_left_index] -= delta_time
                status[self.__chances_left_index] -= 1
        else:
            self.__watch.pop(host, None)

    def update(self, entry):
        host = entry["Host"]
        time = entry["Time"]
        is_blocked = False
        if host in self.__block:
            is_blocked = self.__update_block(entry, host, time)
        else:
            if entry["Request_Type"]=="POST" and entry["Status"] == 401:
                if host in self.__watch:
                    self.__update_watch(entry, host, time)
                else:
                    self.__watch[host] = [time, self.watch_time, self.chances-1]
            else:
                if host in self.__watch:
                    self.__watch.pop(host, None)
        return is_blocked

def time_difference(time1, time2):
    return (time2-time1).total_seconds()

class TestLoginErr(unittest.TestCase):
    def setUp(self):
        time = []
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:01', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:03', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:04', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:06', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:08', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:09', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:11', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:15', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:19', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:21', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:00:10:11', "%d/%b/%Y:%H:%M:%S"))

        self.data = [{"id": 0, "Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[0]},
                {"id": 1, "Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[1]},
                {"id": 2, "Host": "B", "Status": 200, "Request_Type": "POST", "Time": time[2]},
                {"id": 3, "Host": "B", "Status": 200, "Request_Type": "POST", "Time": time[3]},
                {"id": 4, "Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[4]},
                {"id": 5, "Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[5]},
                {"id": 6, "Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[6]},
                {"id": 7, "Host": "B", "Status": 200, "Request_Type": "POST", "Time": time[7]},
                {"id": 8, "Host": "A", "Status": 200, "Request_Type": "POST", "Time": time[8]},
                {"id": 9, "Host": "A", "Status": 401, "Request_Type": "GET",  "Time": time[9]},
                {"id": 10, "Host": "A", "Status": 200, "Request_Type": "POST", "Time": time[10]},
                    ]
        self.time = time

    def test_time_difference(self):
        time1 = dt.datetime.strptime('01/Jul/1995:00:00:01', "%d/%b/%Y:%H:%M:%S")
        time2 = dt.datetime.strptime('02/Jul/1995:03:00:01', "%d/%b/%Y:%H:%M:%S")
        print time_difference(time1, time2)

    def test_update(self):
        blocked = BlockedHosts()
        for entry in self.data:
            is_blocked = blocked.update(entry)
            if is_blocked:
                print entry

if __name__ == '__main__':
        unittest.main()

