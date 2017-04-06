#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to keep track of the activities of each hosts,
and get the n top active hosts.
Global Variables:
    COUNT
    SIZE
Author: Yuan Huang
"""
import unittest
import utility
import random

# COUNT and SIZE are public variables which can be used when set
# the sorting method in the HostActivity.top() function.
# COUNT: The total number of activities
# SIZE: The size of resources that have been requested by the user
COUNT = 0
SIZE = 1

class HostActivity(object):
    """
    The class that record the number of activities and total size of resources by each
    host.
    Example: host = HostActivity()
    """
    # Names for the indices of the list in HostActivity.__host.
    (__COUNT, __SIZE) = (0, 1)
    def __init__(self):
        """
        Contains a dictionary __host with host names as keys and a list as values.
        Private members:
            __host(dict): The dictionary with user IP as its key and a list as value. The list is
               length 2, for example
               list[__COUNT, __SIZE] = (the total number of events of the user,
                                        the total size of resources requested by the user).
        """
        self.__host = {}

    def update(self, entry):
        """Add the info of entry into the statistics of each host.
        Args:
            entry(dict): the dictionary of a log item.
        """
        if entry["Host"] in self.__host:
            self.__host[entry["Host"]][self.__COUNT] += 1
            self.__host[entry["Host"]][self.__SIZE] += entry["Size"]
        else:
            self.__host[entry["Host"]] = [0, 0]
            self.__host[entry["Host"]][self.__COUNT] = 1
            self.__host[entry["Host"]][self.__SIZE] = entry["Size"]

    def top(self, number, sort_method):
        """
        Get the top hosts list with a specified number and sorted by specified feature.
        Args:
            number(int): the number of top hosts.
            sort_method: can only take values COUNT or SIZE.
        Returns:
            A list of tuples. In each tuple, the first element is the count/size, the
            second item is the name of the host.
        Raises:
            NotImplementedError: Error occurs when choosen feature is not COUNT or SIZE.
        """
        if sort_method == COUNT:
            idx = self.__COUNT
        elif sort_method == SIZE:
            idx = self.__SIZE
        else:
            raise NotImplementedError
        keys, values = utility.nlargest_dict(number, self.__host, idx)
        return zip(values, keys)

    def sample(self, number):
        """
        Get the random hosts list with a specified number.
        Args:
            number(int): the number of random hosts.
        Returns:
            A list of strings. Each string is the name of the host.
        """
        keys = random.sample(self.__host.keys(), number)
        return zip(range(len(keys)), keys)

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

    def test_find_active_hosts(self):
        hosts = HostActivity()
        for entry in self.data:
            hosts.update(entry)

        top = hosts.top(1, COUNT)
        self.assertEqual(top[0], (3, "A"))

        top = hosts.top(1, SIZE)
        self.assertEqual(top[0], (33, "E"))

if __name__ == '__main__':
    unittest.main()
