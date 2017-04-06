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
import utility

class TimeStatistics(object):
    """
    The class that keep track of the time window with a fixed period with highest
    number of activities.
    """
    def __init__(self):
        """
        Private variables:
            __daily_hits(dict): A dictionary with date as key and the number of events on
                the given day as its value.
            __daily_hosts(dict): A dictionary with date as key and a set of host names on
                the given day as value.

            __hourly_hits(dict): Hour(int) as key, and number of events as value.
            __hourly_hosts(dict): Hour(int) as key, and a set of host names as value.

        """
        self.__daily_hits = {}
        self.__daily_hosts = {}
        self.__hourly_hits = {}
        self.__hourly_hosts = {}

    def __update_daily_statistics(self, entry):
        """
        Given a new entry, add it to the daily statistics
        """
        date = entry["Time"].date()
        if date not in self.__daily_hits:
            self.__daily_hits[date] =  0
            self.__daily_hosts[date] = set()
        self.__daily_hits[date] += 1
        self.__daily_hosts[date].add(entry["Host"])

    def __update_hourly_statistics(self, entry):
        """
        Given a new entry, add it to the hourly statistics
        """
        hour = entry["Time"].hour
        if hour not in self.__hourly_hits:
            self.__hourly_hits[hour] =  0
            self.__hourly_hosts[hour] = set()
        self.__hourly_hits[hour] += 1
        self.__hourly_hosts[hour].add(entry["Host"])

    def update(self, entry):
        """
        Given a new entry, update the current time window's queue and update the __top_overlap
        list and __top_no_overlap list.
        Args:
            entry(dict): the new log dictionary.
        """
        self.__update_daily_statistics(entry)
        self.__update_hourly_statistics(entry)

    def get_daily_hosts(self):
        """
        Return the statistics for the number of hosts on each day
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of hosts on each day and list[1] as the string of the date.
        """
        result = []
        for day in self.__daily_hosts:
            str_day = day.strftime('%d/%b/%Y')
            result.append([len(self.__daily_hosts[day]), str_day])
        return result

    def get_daily_hits(self):
        """
        Return the statistics for the number of hits on each day
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of hits on each day and list[1] as the string of the date.
        """
        result = []
        for day in self.__daily_hits:
            str_day = day.strftime('%d/%b/%Y')
            result.append([self.__daily_hits[day], str_day])
        return result

    def get_hourly_hosts(self):
        """
        Return the statistics for the number of hosts at different hours of the day
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of hosts on each day and list[1] as the string of the hour.
        """
        result = []
        for hour in self.__hourly_hosts:
            str_hour = time.strftime("%H:%M:%S", time.gmtime(hour*60*60))
            result.append([len(self.__hourly_hosts[hour]), str_hour])
        return result

    def get_hourly_hits(self):
        """
        Return the statistics for the number of hits at different hour during the day
        Returns:
            result(list): A list of length-2 lists. Each length-2 lists contains list[0]
            as the number of hits on each day and list[1] as the string of the hour.
        """
        result = []
        for hour in self.__hourly_hits:
            str_hour = time.strftime("%H:%M:%S", time.gmtime(hour*60*60))
            result.append([self.__hourly_hits[hour], str_hour])
        return result

class TestTimeStatistics(unittest.TestCase):
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
        time_stat = TimeStatistics()
        for entry in self.data:
            time_stat.update(entry)

        hits_per_hour = time_stat.get_hourly_hits()
        self.assertEquals(hits_per_hour[0], [1, "00:00:00"])
        self.assertEquals(hits_per_hour[1], [3, "01:00:00"])

        users_per_hour = time_stat.get_hourly_hosts()
        self.assertEquals(users_per_hour[0], [1, "00:00:00"])
        self.assertEquals(users_per_hour[1], [2, "01:00:00"])

        hits_per_day = time_stat.get_daily_hits()
        self.assertEquals(hits_per_day[0], [11, "01/Jul/1995"])

        users_per_day = time_stat.get_daily_hosts()
        self.assertEquals(users_per_day[0], [2, "01/Jul/1995"])

if __name__ == '__main__':
    unittest.main()
