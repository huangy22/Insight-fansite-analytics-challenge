#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import algorithms
import datetime as dt
from collections import deque

class TimeStatistics(object):
    def __init__(self, hours=1, n_top=10):
        self.time_window = dt.timedelta(hours=hours)
        self.n_top = n_top

        self.__count_index = 0
        self.__time_index = 1

        self.__queue = deque()
        self.__queue.append(dt.datetime.min)

        self.__top = algorithms.LinkedList(self.n_top)
        self.__last_node = algorithms.Node([0, dt.datetime.min])
        self.__top.sorted_insert_node(self.__last_node)
        self.__sorted = True

    def __update_queue(self, entry):
        time = entry["Time"]
        if time > self.__queue[-1]:
            self.__queue.append(time)
            while self.__queue[0] <= self.__queue[-1]-self.time_window:
                self.__queue.popleft()
        else:
            self.__queue.append(time)
        return len(self.__queue), self.__queue[-1]

    def __update_top(self, n, time):
        if time-self.time_window < self.__last_node.data[self.__time_index]:
            if n > self.__last_node.data[self.__count_index]:
                self.__top.replace_data(self.__last_node, [n, time])
                self.__sorted = False
                self.__last_node.data = [n, time]
        else: 
            if not self.__sorted:
                self.__last_node = self.__top.sort_node(self.__last_node)
                self.__sorted = True
            if self.__top.length < self.__top.max_length or n > self.__top.min()[0]:
                self.__last_node = self.__top.sorted_insert_data([n, time])

    def update(self, entry):
        n, time = self.__update_queue(entry)
        self.__update_top(n, time)

    def top(self):
        result = self.__top.get_list()
        for data in result:
            data[1] = (data[1]-self.time_window).strftime("%d/%b/%Y:%H:%M:%S"+ " -0400")
        return result

class TestLoginErr(unittest.TestCase):
    def setUp(self):
        time = []
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:01', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:01:00:03', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:01:00:04', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:02:00:06', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:02:10:06', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:03:00:08', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:05:00:09', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:07:00:11', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:08:00:15', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:08:00:19', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:08:00:21', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:10:10:11', "%d/%b/%Y:%H:%M:%S"))

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


    def test_update_top(self):
        hours = TimeStatistics(hours = 1, n_top = 3)
        for entry in self.data:
            hours.update(entry)
        result = hours.top()
        print result

if __name__ == '__main__':
        unittest.main()


