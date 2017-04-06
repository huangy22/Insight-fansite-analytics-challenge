#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to keep track of the activities of each hosts,
and block the host for a period of time if the host performs n
consecutive failed login attempts over 20 seconds.
Author: Yuan Huang
"""
import unittest
import datetime as dt

class BlockedHosts(object):
    """
    The class that keeps track of the failed login and block further activities if a host
    fails to login for a number of times consecutively within a specified time window.
    """
    # Private Constants:
    # The name of indices in the monitor_dict and block_dict.
    (__LAST_EVENT, __TIME_LEFT, __CHANCES_LEFT) = (0, 1, 2)
    def __init__(self, monitor_seconds=20, block_seconds=300, chances=3):
        """
        Public variables:
            monitor_time: the time period during which a number of failed login attempts will
                trigger the block event
            block_time: the time period to block the user
            chances: the number of attempts of failed login
        Private variables:
            __monitor_dict(dict): keep track the events after first failed login happens, key: host name,
                value: a list, [time of last post, monitor time left, chances left]
            __block_dict(dict): keep track the events after the user gets blocked, key: host name,
                value: a list, [time of last post, monitor time left, chances left]
        """
        self.__monitor_time = monitor_seconds
        self.__block_time = block_seconds
        self.__chances = chances

        self.__monitor = {}
        self.__block = {}

    def __update_block(self, host, time):
        """
        For a new entry of a host already in block dictionary, check if the entry needs to be
        blocked and update the block dictionary accordingly.
        Args:
            host(str): the host name of the entry. The host is already in the block dictionary.
            time(datetime): the time of the new entry.
        Returns:
            is_blocked: True if the entry needs to be blocked; False otherwise.
        """
        is_blocked = False
        if host in self.__block:
            status = self.__block[host]
            delta_time = time_difference(status[self.__LAST_EVENT], time)
            if delta_time <= status[self.__TIME_LEFT]:
                is_blocked = True
                status[self.__LAST_EVENT] = time
                status[self.__TIME_LEFT] -= delta_time
            else:
                self.__block.pop(host, None)
        return is_blocked

    def __update_monitor(self, host, time):
        """
        For a new entry of a host already in the monitor dictionary, check if the entry needs to be
        added to block dictionary and update the monitor dictionary accordingly.
        Args:
            host(str): the host name of the entry. The host is already in the monitor dictionary.
            time(datetime): the time of the new entry.
        """
        status = self.__monitor[host]
        delta_time = time_difference(status[self.__LAST_EVENT], time)
        if delta_time <= status[self.__TIME_LEFT]:
            if status[self.__CHANCES_LEFT] == 1:
                self.__monitor.pop(host, None)
                self.__block[host] = [time, self.__block_time]
            else:
                status[self.__LAST_EVENT] = time
                status[self.__TIME_LEFT] -= delta_time
                status[self.__CHANCES_LEFT] -= 1
        else:
            self.__monitor.pop(host, None)

    def update(self, entry):
        """
        Given a new entry, update the status of monitor and block dictionaries. Return whether the
        entry needs to be blocked.
        Args:
            entry(dict): A Apache log dictionary.
        Returns:
            is_blocked: True if the entry needs to be blocked; False otherwise.
        """
        host = entry["Host"]
        time = entry["Time"]
        is_blocked = False
        if host in self.__block:
            is_blocked = self.__update_block(host, time)
        else:
            if entry["Request"] == "/login" and entry["Status"] == 401:
                if host in self.__monitor:
                    self.__update_monitor(host, time)
                else:
                    self.__monitor[host] = [time, self.__monitor_time, self.__chances-1]
            else:
                if host in self.__monitor:
                    self.__monitor.pop(host, None)
        return is_blocked

def time_difference(time_before, time_after):
    """
    Calculate the difference between two time variables in units of seconds.
    Args:
        time_before(datetime): time variable that happens earlier
        time_after(datetime): time variable that happens later
    Returns:
        diff_time(float): the time difference in units of seconds
    """
    return (time_after-time_before).total_seconds()

class TestBlockedHosts(unittest.TestCase):
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

        self.data = [{"Host": "A", "Status": 401, "Request": "/login", "Time": time[0]},
                     {"Host": "A", "Status": 401, "Request": "/login", "Time": time[1]},
                     {"Host": "B", "Status": 200, "Request": "/login", "Time": time[2]},
                     {"Host": "B", "Status": 200, "Request": "/login", "Time": time[3]},
                     {"Host": "A", "Status": 401, "Request": "/login", "Time": time[4]},
                     {"Host": "A", "Status": 401, "Request": "/login", "Time": time[5]},
                     {"Host": "A", "Status": 401, "Request": "/login", "Time": time[6]},
                     {"Host": "B", "Status": 200, "Request": "/login", "Time": time[7]},
                     {"Host": "A", "Status": 200, "Request": "/login", "Time": time[8]},
                     {"Host": "A", "Status": 401, "Request": "/item", "Time": time[9]},
                     {"Host": "A", "Status": 200, "Request": "/login", "Time": time[10]},
                    ]
        self.time = time

    def test_time_difference(self):
        time1 = dt.datetime.strptime('01/Jul/1995:00:00:01', "%d/%b/%Y:%H:%M:%S")
        time2 = dt.datetime.strptime('02/Jul/1995:03:00:01', "%d/%b/%Y:%H:%M:%S")
        #difference is one day and three hours
        self.assertEqual(time_difference(time1, time2), 24*60*60+3*60*60)

    def test_update(self):
        blocked = BlockedHosts()
        id_list = []
        #for entry in self.data:
        for i in range(len(self.data)):
            entry = self.data[i]
            is_blocked = blocked.update(entry)
            if is_blocked:
                id_list.append(i)
        self.assertEqual(tuple(id_list), (5, 6, 8, 9))
                #log.info("UnitTest: To block: {0}".format(entry))

if __name__ == '__main__':
    unittest.main()
