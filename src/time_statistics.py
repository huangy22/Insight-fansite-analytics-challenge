#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to keep track of the number of activities in a fixed
time window, and get the top n busiest periods that have the most activities.
Author: Yuan Huang
"""
import unittest
import datetime as dt
from collections import deque
import algorithms

class TimeStatistics(object):
    """
    The class that keep track of the time window with a fixed period with highest
    number of activities.
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, hours=1, n_top=10):
        """
        Public variables:
            time_window(timedelta): the length of the specified time window
            n_top(int): the number of top time periods to keep track on
        Private variables:
            __queue(deque): the time of each activity in the current time window
            __top(linked list): an ascending ordered list that stores the top n
                time window's ending time. The data on each node of the linked list
                is a list. List[__count_index] stores the number of activities, while
                list[__time_index] stores the ending time of this time period.
            __last_node(node): the node with the latest time window pushed into the
                top list.
            __sorted(boolean): True if the linked list is in ascending order, False if
                the node __last_node is not in place but the rest of the list is in
                ascending order.
        """
        self.time_window = dt.timedelta(hours=hours)
        self.n_top = n_top

        self.__count_index = 0
        self.__time_index = 1

        self.__queue = deque()

        self.__top = algorithms.LinkedList(self.n_top)
        self.__last_node = algorithms.Node([0, dt.datetime.min])
        self.__sorted = True

        self.__queue.append(dt.datetime.min)
        self.__top.sorted_insert_node(self.__last_node)

    def __update_queue(self, entry):
        """
        Given a new entry, push it into the queue of the current window and pop
        the earlier posts that is no longer in the window.
        Args:
            entry(dict): the new log dictionary.
        Returns:
            n(int): number of logs in the queue
            time(datetime): the time of last entry in the queue
        """
        time = entry["Time"]
        if time > self.__queue[-1]:
            self.__queue.append(time)
            while self.__queue[0] <= self.__queue[-1]-self.time_window:
                self.__queue.popleft()
        else:
            self.__queue.append(time)
        return len(self.__queue), self.__queue[-1]

    def __update_top(self, number, time):
        """
        Given the number of logs and ending time of the current time window,
        update the __top list.
        Args:
            number(int): number of activities in the current queue.
            time(datetime): ending time in the current queue.
        """

        # Check whether the current time window overlaps with others in __top
        if time-self.time_window < self.__last_node.data[self.__time_index]:
            # The time window overlaps with the last time window pushed to __top
            if number > self.__last_node.data[self.__count_index]:
                # Replace the number of logs if the current number is larger
                self.__last_node.replace_data([number, time])
                self.__sorted = False
                self.__last_node.data = [number, time]
        else:
            # The time window doesn't overlap with any time windows in __top
            if not self.__sorted:
                # Put the __last_node in the right place in the list
                self.__last_node = self.__top.sort_node(self.__last_node)
                self.__sorted = True

            if self.__top.length < self.__top.max_length or number > self.__top.min()[0]:
                # Push the current time window to the top list when the top list is not
                # full or the number of logs is larger than the smallest in the top list
                self.__last_node = self.__top.sorted_insert_data([number, time])

    def update(self, entry):
        """
        Given a new entry, update the current time window's queue and update the __top
        list.
        Args:
            entry(dict): the new log dictionary.
        """
        number, time = self.__update_queue(entry)
        self.__update_top(number, time)

    def top(self):
        """
        Transform the __top (ascending linked list) to a list in descending order.
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of activities of the time window and list[1] the starting time.
        """
        result = self.__top.get_list(order="descend")
        for data in result:
            data[1] = (data[1]-self.time_window).strftime("%d/%b/%Y:%H:%M:%S"+ " -0400")
        return result

class TestTime(unittest.TestCase):
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

        self.data = [{"Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[0]},
                     {"Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[1]},
                     {"Host": "B", "Status": 200, "Request_Type": "POST", "Time": time[2]},
                     {"Host": "B", "Status": 200, "Request_Type": "POST", "Time": time[3]},
                     {"Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[4]},
                     {"Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[5]},
                     {"Host": "A", "Status": 401, "Request_Type": "POST", "Time": time[6]},
                     {"Host": "B", "Status": 200, "Request_Type": "POST", "Time": time[7]},
                     {"Host": "A", "Status": 200, "Request_Type": "POST", "Time": time[8]},
                     {"Host": "A", "Status": 401, "Request_Type": "GET", "Time": time[9]},
                     {"Host": "A", "Status": 200, "Request_Type": "POST", "Time": time[10]},
                    ]
        self.time = time


    def test_update_top(self):
        hours = TimeStatistics(hours=1, n_top=3)
        for entry in self.data:
            hours.update(entry)
        result = hours.top()
        self.assertEquals(result[0], [3, '01/Jul/1995:07:00:21 -0400'])
        self.assertEquals(result[1], [2, '01/Jul/1995:01:10:06 -0400'])
        self.assertEquals(result[2], [2, '01/Jul/1995:00:00:04 -0400'])

if __name__ == '__main__':
    unittest.main()
