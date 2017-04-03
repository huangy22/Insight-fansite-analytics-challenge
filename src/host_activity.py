#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to keep track of the activities of each hosts,
and get the n top active hosts.
Author: Yuan Huang
"""
import unittest
import algorithms

class HostActivity(object):
    def __init__(self):

        self.count = 0
        self.size = 1

        self.__count_index = 0
        self.__size_index = 1

        self.__host = {}

    def update(self, entry):
        """Add the info of entry into the statistics of each host.
        Args:
            entry(dict): the dictionary of a log info, including keys "Host", "Time",
            "Request", "Reply", "Size".
        Returns:
            None.
        """
        if entry["Host"] in self.__host:
            self.__host[entry["Host"]][self.__count_index] += 1
            self.__host[entry["Host"]][self.__size_index] += entry["Size"]
        else:
            self.__host[entry["Host"]] = [0, 0]
            self.__host[entry["Host"]][self.__count_index] = 1
            self.__host[entry["Host"]][self.__size_index] = entry["Size"]

    def top(self, number, feature):
        if feature == self.count:
            idx = self.__count_index
        elif feature == self.size:
            idx = self.__size_index
        else:
            raise NotImplementedError
        keys, values = algorithms.nlargest_dict(number, self.__host, idx)
        return zip(values, keys)

    def get(self, host, feature):
        if feature == self.count:
            idx = self.__count_index
        elif feature == self.size:
            idx = self.__size_index
        else:
            raise NotImplementedError
        return self.__host[host][idx]

class TestHost(unittest.TestCase):
    def setUp(self):
        self.data = [{"Host": "A", "Size": 1},
                     {"Host": "A", "Size": 2},
                     {"Host": "A", "Size": 2},
                     {"Host": "B", "Size": 20},
                     {"Host": "B", "Size": 3},
                     {"Host": "C", "Size": 2},
                     {"Host": "C", "Size": 2},
                     {"Host": "D", "Size": 2},
                     {"Host": "E", "Size": 33},
                     {"Host": "F", "Size": 2}]

    def test_update_host(self):
        hosts = HostActivity()
        for entry in self.data:
            hosts.update(entry)
        self.assertEqual(hosts.get("A", hosts.count), 3)

    def test_find_active_hosts(self):
        hosts = HostActivity()
        for entry in self.data:
            hosts.update(entry)

        top = hosts.top(1, hosts.count)
        self.assertEqual(top[0], (3, "A"))

        top = hosts.top(1, hosts.size)
        self.assertEqual(top[0], (33, "E"))

if __name__ == '__main__':
    unittest.main()
