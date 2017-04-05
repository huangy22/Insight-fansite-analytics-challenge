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
import data_structures

class TimeStatistics(object):
    """
    The class that keep track of the time window with a fixed period with highest
    number of activities.
    Args:
        hours(float): the length of time window in unit of hours
        n_top(int): the number of time windows with most activities
    Public variables:
        time_window(timedelta): the length of the time window
        n_top(int): the number of top time periods to keep track on
    """
    # 
    (__COUNT, __TIME) = (0, 1)
    def __init__(self, hours=1, n_top=10):
        """
        Private variables:
            __queue(deque): a queue stores the time of each activity in the current time window
            __top_overlap(LinkedList): an ascending ordered linked list that stores the top n
                time window's starting time. 
            __top_no_overlap(LinkedList): an ascending ordered linked list that stores the top n
                time window's starting time. Each time window doesn't overlap with each other. 
            __last_node(node): the node with the latest time window pushed into the
                top list.
            __sorted(boolean): True if the linked list is in ascending order, False if
                the node __last_node is not in place but the rest of the list is in
                ascending order.
        """
        self.time_window = dt.timedelta(hours=hours)
        self.n_top = n_top

        self.__queue = deque()

        self.__top_overlap = data_structures.LinkedList(self.n_top)

        self.__last_node = None
        self.__sorted = True
        self.__top_no_overlap = data_structures.LinkedList(self.n_top)

        self.__daily = {}

    def __update_queue(self, entry):
        """
        Given a new entry, push it into the queue of the current window and pop
        the earlier posts that is no longer in the window. Returns a list of completed
        time windows with its number of logs and starting time.
        Args:
            entry(dict): the new log dictionary.
        Returns:
            datalist(list): A list of length-2 lists, e.g. [number, time]. number(int) is number
            of logs in a last time window; time(datetime) is the starting
            time of a time window.
        """
        time = entry["Time"]

        # Push the new event into the queue
        self.__queue.append(time)

        datalist = []
        n_same_time = 0
        if len(self.__queue) > 0:
            # Check if the new time exceeds the previous time window
            endtime = self.__queue[0] + self.time_window
            if time >= endtime:
                # Pop out the oldest events in the queue to make the duration of the queue
                # smaller than the time window
                while len(self.__queue) > 1 and self.__queue[0] <= time-self.time_window:
                    head = self.__queue.popleft()
                    # Append the number and starting time to the return list
                    if head != self.__queue[0]:
                        datalist.append([len(self.__queue) + n_same_time, head])
                        n_same_time = 0
                    else:
                        n_same_time += 1
        return datalist

    def __update_top(self, number, time):
        """
        Given the number of logs and starting time of the current time window,
        update the __top_overlap list.
        Args:
            number(int): number of activities in the current queue.
            time(datetime): starting time in the current queue.
        """
        new_data = [number, time]
        if self.__top_overlap.length < self.__top_overlap.max_length or\
            tuple(new_data) > tuple(self.__top_overlap.min()):
            self.__top_overlap.sorted_insert_data(new_data)

    def __update_top_without_overlap(self, number, time):
        """
        Given the number of logs and starting time of the current time window,
        update the __top_no_overlap list. The time windows in __top_no_overlap don't
        overlap with each other.
        Args:
            number(int): number of activities in the current queue.
            time(datetime): starting time in the current queue.
        """

        new_data = [number, time]
        if self.__last_node is None:
            self.__last_node = self.__top_no_overlap.sorted_insert_data(new_data)
        else:
            # Check whether the current time window overlaps with others in __top_overlap
            if time - self.time_window < self.__last_node.data[self.__TIME]:

                # The time window overlaps with the last time window pushed to __top_overlap
                if tuple(new_data) > tuple(self.__last_node.data):
                    # Replace the number of logs if the current number is larger
                    self.__last_node.replace_data(new_data)
                    self.__sorted = False
                    self.__last_node.data = new_data

            else:
                # The time window doesn't overlap with any time windows in __top_overlap
                if not self.__sorted:
                    # Put the __last_node in the right place in the list
                    self.__last_node = self.__top_no_overlap.sort_node(self.__last_node)
                    self.__sorted = True

                if self.__top_no_overlap.length < self.__top_no_overlap.max_length\
                   or tuple(new_data) > tuple(self.__top_no_overlap.min()):

                    # Push the current time window to the top list when the top list is not
                    # full or the number of logs is larger than the smallest in the top list
                    self.__last_node = self.__top_no_overlap.sorted_insert_data(new_data)

    def __update_daily_statistics(self, entry):
        """
        Given a new entry, add it to the daily statistics
        """
        today = entry["Time"].date()
        if today in self.__daily:
            self.__daily[today]["hits"] += 1
            self.__daily[today]["users"].add(entry["Host"])
        else:
            self.__daily[today] = {"hits": 0, "users": set()}

    def update(self, entry):
        """
        Given a new entry, update the current time window's queue and update the __top_overlap
        list and __top_no_overlap list.
        Args:
            entry(dict): the new log dictionary.
        """
        self.__update_daily_statistics(entry)
        window_list  = self.__update_queue(entry)
        for (number, time) in window_list:
            self.__update_top(number, time)
            self.__update_top_without_overlap(number, time)

    def finalize(self, entry):
        """
        At the end of file, collect the time windows that is not with one full hour
        but contains the events in the last period of time.
        """
        fake_entry = entry
        fake_entry["Time"] = entry["Time"] + self.time_window
        self.update(fake_entry)

    def top(self):
        """
        Transform the __top_overlap (ascending linked list) to a list in descending order.
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of activities of the time window and list[1] the starting time.
        """
        result = self.__top_overlap.get_list(order="descend")
        for data in result:
            data[1] = data[1].strftime("%d/%b/%Y:%H:%M:%S %z")
        return result

    def top_no_overlap(self):
        """
        Transform the __top_no_overlap (ascending linked list) to a list in descending order.
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of activities of the time window and list[1] the starting time.
        """
        result = self.__top_no_overlap.get_list(order="descend")
        for data in result:
            data[1] = data[1].strftime("%d/%b/%Y:%H:%M:%S %z")
        return result

    def get_daily_users(self):
        """
        Return the statistics for the number of users on each day
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of users on each day and list[1] as the string of the date.
        """
        result = []
        for day in self.__daily:
            str_day = day.strftime('%d/%b/%Y')
            result.append([len(self.__daily[day]["users"]), str_day])
        return result

    def get_daily_hits(self):
        """
        Return the statistics for the number of hits on each day
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of hits on each day and list[1] as the string of the date.
        """
        result = []
        for day in self.__daily:
            str_day = day.strftime('%d/%b/%Y')
            result.append([self.__daily[day]["hits"], str_day])
        return result

class TestTime(unittest.TestCase):
    def setUp(self):
        time = []
        time.append(dt.datetime.strptime('01/Jul/1995:00:00:01', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:01:00:03', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:01:00:04', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:01:00:08', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:02:00:06', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:02:10:06', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:08:00:11', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:08:00:11', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:08:00:13', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:08:00:13', "%d/%b/%Y:%H:%M:%S"))
        time.append(dt.datetime.strptime('01/Jul/1995:08:00:15', "%d/%b/%Y:%H:%M:%S"))

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
            final = entry
            hours.update(entry)
        hours.finalize(final)

        result = hours.top()
        self.assertEquals(result[0], [5, '01/Jul/1995:08:00:11 '])
        self.assertEquals(result[1], [3, '01/Jul/1995:08:00:13 '])
        self.assertEquals(result[2], [3, '01/Jul/1995:01:00:03 '])

        result2 = hours.top_no_overlap()
        self.assertEquals(result2[0], [5, '01/Jul/1995:08:00:11 '])
        self.assertEquals(result2[1], [3, '01/Jul/1995:01:00:03 '])
        self.assertEquals(result2[2], [2, '01/Jul/1995:02:00:06 '])

        hits = hours.get_daily_hits()
        self.assertEquals(hits[0], [11, "01/Jul/1995"])

        users = hours.get_daily_users()
        self.assertEquals(users[0], [2, "01/Jul/1995"])

if __name__ == '__main__':
    unittest.main()
