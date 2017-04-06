#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to keep track of the number of activities in a fixed
time window, and get the top n busiest periods that have the most activities.
Author: Yuan Huang
"""
import unittest
import datetime as dt
import time
from collections import deque
import heapq
import utility

class TimeWindow(object):
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
    # Names for the indices of the list in TimeWindow.__top_overlap and TimeWindow.__top_no_overlap.
    (__COUNT, __TIME) = (0, 1)
    def __init__(self, hours=1, n_top=10):
        """
        Private variables:
            __queue(deque): a queue stores the time of each activity in the current time window
            __top_overlap(Heap): an ascending ordered heap that stores the top n
                time window's starting time. 
            __top_no_overlap(Heap): an ascending ordered heap that stores the top n
                time window's starting time. Each time window doesn't overlap with each other. 
            __pending_data(list): the list of length 2 with indices name __COUNT and __TIME
            __is_pending(boolean): True if there is a pending data that has not yet been pushed
                to the heap.
        """
        self.__time_window = dt.timedelta(hours=hours)
        self.__n_top = n_top

        self.__queue = deque()

        self.__top_overlap = utility.Heap(self.__n_top) 

        self.__is_pending = False
        self.__pending_data = None

        self.__top_no_overlap = utility.Heap(self.__n_top)

    def __shift_time_window(self, entry):
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
            endtime = self.__queue[0] + self.__time_window
            if time >= endtime:
                # Pop out the oldest events in the queue to make the duration of the queue
                # smaller than the time window
                while len(self.__queue) > 1 and self.__queue[0] <= time-self.__time_window:
                    head = self.__queue.popleft()
                    # Append the number and starting time to the return list
                    if head != self.__queue[0]:
                        datalist.append([len(self.__queue) + n_same_time, head])
                        n_same_time = 0
                    else:
                        n_same_time += 1
        return datalist

    def __update_top_allow_overlap(self, number, time):
        """
        Given the number of logs and starting time of the current time window,
        update the __top_overlap heap.
        Args:
            number(int): number of activities in the current queue.
            time(datetime): starting time in the current queue.
        """
        new_data = [number, time]
        self.__top_overlap.push(new_data) 

    def __update_top_without_overlap(self, number, time):
        """
        Given the number of logs and starting time of the current time window,
        update the __top_no_overlap heap. The time windows in __top_no_overlap don't
        overlap with each other.
        Args:
            number(int): number of activities in the current queue.
            time(datetime): starting time in the current queue.
        """

        new_data = [number, time]

        # Check if the current time window overlaps with the pending time window
        if self.__is_pending and time - self.__time_window < self.__pending_data[self.__TIME]:

            # Check if the current number is larger than the pending time window data
            if tuple(new_data) > tuple(self.__pending_data):
                # Replace the number of logs if the current number is larger
                self.__pending_data = new_data

        else:

            # Check if there is a pending data that needs to be pushed into the top list
            if self.__is_pending:
                # Put the __pending_data in the right place in the list
                self.__top_no_overlap.push(self.__pending_data)
                self.__is_pending = False
                self.__pending_data = None

            # Check if the current time window can potentially be pushed
            # Namingly if the top list is not full or the number is larger than the smallest
            # in the list
            if self.__top_no_overlap.length() < self.__n_top\
               or tuple(new_data) > tuple(self.__top_no_overlap.min()):

                # Record current time window as a pending time window
                self.__is_pending = True
                self.__pending_data = new_data

    def update(self, entry):
        """
        Given a new entry, update the current time window's queue and update the __top_overlap
        heap and __top_no_overlap heap.
        Args:
            entry(dict): the new log dictionary.
        """
        window_list  = self.__shift_time_window(entry)
        for (number, time) in window_list:
            self.__update_top_allow_overlap(number, time)
            self.__update_top_without_overlap(number, time)

    def finalize(self, entry):
        """
        At the end of file, collect the time windows that is not with one full hour
        but contains the events in the last period of time.
        """
        # Make up a fake entry at the end of file
        fake_entry = entry

        # Set the time to be one hour later than the last time in the file
        fake_entry["Time"] = entry["Time"] + self.__time_window

        # Update the fake entry data so that the time windows in the last hour can be added
        # to the list
        self.update(fake_entry)

        # Check if there is a pending data that needs to be pushed into the 
        # __top_no_overlap list
        if self.__is_pending:
            # Put the __pending_data in the right place in the list
            self.__top_no_overlap.push(self.__pending_data)
            self.__is_pending = False
            self.__pending_data = None

    def top(self):
        """
        Transform the __top_overlap (min heap) to a list in descending order.
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of activities of the time window and list[1] the starting time.
        """
        result = self.__top_overlap.get()
        for data in result:
            data[1] = data[1].strftime("%d/%b/%Y:%H:%M:%S %z")
        return result

    def top_no_overlap(self):
        """
        Transform the __top_no_overlap (min heap) to a list in descending order.
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of activities of the time window and list[1] the starting time.
        """
        result = self.__top_no_overlap.get()
        for data in result:
            data[1] = data[1].strftime("%d/%b/%Y:%H:%M:%S %z")
        return result


class TestTimeWindow(unittest.TestCase):
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
        hours = TimeWindow(hours=1, n_top=3)

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

if __name__ == '__main__':
    unittest.main()
