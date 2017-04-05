#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to keep track of the get requests of each resources,
and get the top n resources that consumes the most bandwidth.
Author: Yuan Huang
"""
import unittest
import utility

COUNT = 0
SIZE = 1
BANDWIDTH = 2

class ResourceStatistics(object):
    """
    The class that records the information for each resources, including
    the times of request, the size and consumed bandwidth.
    """
    def __init__(self):
        """
        Contains a dictionary __resource with resource names as keys and a list as values.
        The value list has three items: value[__count_index] is the times of request
        for each resource, value[__size_index] is the size of resource,
        value[__bandwidth_index] is the bandwidth consumed by each resource..

        Count, size, bandwidth are public variables which can be used when assigning
        the feature to sort by in the top() function.
        """
        self.__count_index = 0
        self.__size_index = 1
        self.__bandwidth_index = 2

        self.__resource = {}

    def update(self, entry):
        """Add the info of entry into the statistics of each resource.
        Args:
            entry(dict): the dictionary of a log info
        """
        res = entry["Request"]

        if res != "/":
            if res in self.__resource:
                self.__resource[res][self.__count_index] += 1
                self.__resource[res][self.__bandwidth_index] += entry["Size"]
                self.__resource[res][self.__size_index] = self.__resource[res]\
                    [self.__bandwidth_index]/float(self.__resource[res][self.__count_index])
            else:
                self.__resource[res] = [0, 0, 0]
                self.__resource[res][self.__count_index] = 1
                self.__resource[res][self.__size_index] = float(entry["Size"])
                self.__resource[res][self.__bandwidth_index] = entry["Size"]

    def bottom(self, number, feature):
        """
        Get the top resources list with a specified number and sorted by specified feature.
        Args:
            number(int): the number of top resources.
            feature: can only take values COUNT, SIZE or BANDWIDTH.
        Returns:
            A list of tuples. In each tuple, the first element is the count/size/bandwidth, the
            second item is the name of the resource.
        Raises:
            NotImplementedError: Error occurs when choosen feature is not COUNT,
            SIZE, or BANDWIDTH.
        """
        if feature == COUNT:
            idx = self.__count_index
        elif feature == BANDWIDTH:
            idx = self.__bandwidth_index
        elif feature == SIZE:
            idx = self.__size_index
        else:
            raise NotImplementedError
        keys, values = utility.nsmallest_dict(number, self.__resource, idx)
        return zip(values, keys)

    def top(self, number, feature):
        """
        Get the top resources list with a specified number and sorted by specified feature.
        Args:
            number(int): the number of top resources.
            feature: can only take values COUNT, SIZE or BANDWIDTH.
        Returns:
            A list of tuples. In each tuple, the first element is the count/size/bandwidth, the
            second item is the name of the resource.
        Raises:
            NotImplementedError: Error occurs when choosen feature is not COUNT,
            SIZE, or BANDWIDTH.
        """
        if feature == COUNT:
            idx = self.__count_index
        elif feature == BANDWIDTH:
            idx = self.__bandwidth_index
        elif feature == SIZE:
            idx = self.__size_index
        else:
            raise NotImplementedError
        keys, values = utility.nlargest_dict(number, self.__resource, idx)
        return zip(values, keys)

    def get(self, resource, feature):
        """
        Get the specified feature of a certain host.
        Args:
            feature: can only take values COUNT, SIZE, BANDWIDTH.
        Returns:
            the value of the feature of the resource.
        Raises:
            NotImplementedError: Error occurs when choosen feature is not COUNT,
            SIZE or BANDWIDTH.
        """
        if feature == COUNT:
            idx = self.__count_index
        elif feature == BANDWIDTH:
            idx = self.__bandwidth_index
        elif feature == SIZE:
            idx = self.__size_index
        else:
            raise NotImplementedError
        return self.__resource[resource][idx]


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

    def test_update_resource(self):
        resources = ResourceStatistics()
        for entry in self.data:
            resources.update(entry)
        self.assertEqual(resources.get("A", COUNT), 3)
        self.assertEqual(resources.get("A", SIZE), 5.0/3)
        self.assertEqual(resources.get("A", BANDWIDTH), 5)

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
