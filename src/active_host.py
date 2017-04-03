#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import algorithms 
import read_entry

class HostActivity(object):
    def __init__(self):

        self.COUNT = 0
        self.SIZE = 1

        self.__count_index = 0
        self.__size_index = 1

        self.__host= {}

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
        if feature==self.COUNT:
            idx = self.__count_index 
        elif feature==self.SIZE:
            idx = self.__size_index
        else:
            raise NotImplementedError
        return algorithms.nlargest_dict(number, self.__host, idx)

    def get(self, host, feature):
        if feature==self.COUNT:
            idx = self.__count_index 
        elif feature==self.SIZE:
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
                    {"Host": "F", "Size": 2},
                    ]

    def test_update_host(self):
        hosts = HostActivity()
        for entry in self.data:
            hosts.update(entry)
        print "A: ", hosts.get("A", hosts.COUNT)

    def test_find_active_hosts(self):
        hosts = HostActivity()
        for entry in self.data:
            hosts.update(entry)
        print hosts.top(1, hosts.COUNT)
        print hosts.top(1, hosts.SIZE)

if __name__ == '__main__':
        unittest.main()
