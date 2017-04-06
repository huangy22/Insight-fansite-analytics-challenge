#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to keep track of the get requests of each resources,
and get the top n resources that consumes the most bandwidth.
Author: Yuan Huang
"""
import unittest
import utility

# COUNT, SIZE, BANDWIDTH are public variables which can be used when set
# the sorting method in the ResourceStatistics.top() function.

# COUNT: The total number of requests for each resource
COUNT = 0
# SIZE: The size of resource
SIZE = 1
# BANDWIDTH: The total network traffic for this resource
BANDWIDTH = 2

class ResourceStatistics(object):
    """
    The class that records the information for each resources, including
    the times of request, the size and consumed bandwidth.
    """
    # Names for the indices of the list in ResourceStatistics.__resource.
    (__COUNT, __SIZE, __BANDWIDTH) = (0, 1, 2)
    def __init__(self):
        """
        Private members:
            __resource(dict): The dictionary with resource name as its key and a list as value. The list is
               length 3, for example
               list[__COUNT, __SIZE, __BANDWIDTH] = (the total number of requests of the resource,
                                                     the size of resource,
                                                     total network traffic for the resource).
        """
        self.__resource = {}

    def update(self, entry):
        """Add the info of entry into the statistics of each resource.
        Args:
            entry(dict): the dictionary of a log info
        """
        res = entry["Request"]

        if res != "/":
            if res in self.__resource:
                self.__resource[res][self.__COUNT] += 1
                self.__resource[res][self.__BANDWIDTH] += entry["Size"]
                self.__resource[res][self.__SIZE] = self.__resource[res]\
                    [self.__BANDWIDTH]/float(self.__resource[res][self.__COUNT])
            else:
                self.__resource[res] = [0, 0, 0]
                self.__resource[res][self.__COUNT] = 1
                self.__resource[res][self.__SIZE] = float(entry["Size"])
                self.__resource[res][self.__BANDWIDTH] = entry["Size"]

    def bottom(self, number, sort_method):
        """
        Get the top resources list with a specified number and sorted by specified feature.
        Args:
            number(int): the number of top resources.
            sort_method: can only take values COUNT, SIZE or BANDWIDTH.
        Returns:
            A list of tuples. In each tuple, the first element is the count/size/bandwidth, the
            second item is the name of the resource.
        Raises:
            NotImplementedError: Error occurs when choosen feature is not COUNT,
            SIZE, or BANDWIDTH.
        """
        if sort_method == COUNT:
            idx = self.__COUNT
        elif sort_method == BANDWIDTH:
            idx = self.__BANDWIDTH
        elif sort_method == SIZE:
            idx = self.__SIZE
        else:
            raise NotImplementedError
        keys, values = utility.nsmallest_dict(number, self.__resource, idx)
        return zip(values, keys)

    def top(self, number, sort_method):
        """
        Get the top resources list with a specified number and sorted by specified feature.
        Args:
            number(int): the number of top resources.
            sort_method: can only take values COUNT, SIZE or BANDWIDTH.
        Returns:
            A list of tuples. In each tuple, the first element is the count/size/bandwidth, the
            second item is the name of the resource.
        Raises:
            NotImplementedError: Error occurs when choosen feature is not COUNT,
            SIZE, or BANDWIDTH.
        """
        if sort_method == COUNT:
            idx = self.__COUNT
        elif sort_method == BANDWIDTH:
            idx = self.__BANDWIDTH
        elif sort_method == SIZE:
            idx = self.__SIZE
        else:
            raise NotImplementedError
        keys, values = utility.nlargest_dict(number, self.__resource, idx)
        return zip(values, keys)

class TestResource(unittest.TestCase):
    def setUp(self):
        self.data = [{"Request": "A", "Size": 1},
                     {"Request": "A", "Size": 2},
                     {"Request": "A", "Size": 2},
                     {"Request": "B", "Size": 20},
                     {"Request": "B", "Size": 3},
                     {"Request": "C", "Size": 2},
                     {"Request": "C", "Size": 2},
                     {"Request": "D", "Size": 2},
                     {"Request": "E", "Size": 33},
                     {"Request": "F", "Size": 2},
                    ]

    def test_find_small_resources(self):
        resources = ResourceStatistics()
        for entry in self.data:
            resources.update(entry)
        bottom = resources.bottom(2, COUNT)
        self.assertEqual(bottom[0], (1, "D"))
        self.assertEqual(bottom[1], (1, "E"))

        bottom = resources.bottom(2, BANDWIDTH)
        self.assertEqual(bottom[0], (2, "D"))
        self.assertEqual(bottom[1], (2, "F"))

        bottom = resources.bottom(2, SIZE)
        self.assertEqual(bottom[0], (5.0/3, "A"))
        self.assertEqual(bottom[1], (2.0, "C"))

    def test_find_large_resources(self):
        resources = ResourceStatistics()
        for entry in self.data:
            resources.update(entry)
        top = resources.top(2, COUNT)
        self.assertEqual(top[0], (3, "A"))
        self.assertEqual(top[1], (2, "C"))

        top = resources.top(2, BANDWIDTH)
        self.assertEqual(top[0], (33, "E"))
        self.assertEqual(top[1], (23, "B"))

        top = resources.top(2, SIZE)
        self.assertEqual(top[0], (33, "E"))
        self.assertEqual(top[1], (11.5, "B"))

if __name__ == '__main__':
    unittest.main()
