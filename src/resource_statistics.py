#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import algorithms

class ResourceStatistics(object):
    def __init__(self):
        self.COUNT = 0
        self.SIZE = 1
        self.BANDWIDTH = 2
        
        self.__count_index = 0
        self.__size_index = 1
        self.__bandwidth_index = 2

        self.__resource = {}

    def update(self, entry):
        """Add the info of entry into the statistics of each resource.
        Args:
            entry(dict): the dictionary of a log info, including keys "Host", "Time",
            "Request", "Reply", "Size".
        Returns:
            None.
        """
        res = entry["Request"]

        if res != "/":
            if res in self.__resource:
                self.__resource[res][self.__count_index] += 1 
                self.__resource[res][self.__bandwidth_index] += entry["Size"]
                self.__resource[res][self.__size_index] = self.__resource[res][self.__bandwidth_index]\
                    /self.__resource[res][self.__count_index]
            else:
                self.__resource[res] =  [0, 0, 0]
                self.__resource[res][self.__count_index] = 1 
                self.__resource[res][self.__size_index] = entry["Size"]
                self.__resource[res][self.__bandwidth_index] = entry["Size"]

    def top(self, number, feature):
        if feature == self.COUNT:
            idx = self.__count_index 
        elif feature == self.BANDWIDTH:
            idx = self.__bandwidth_index
        elif feature == self.SIZE:
            idx = self.__size_index
        else:
            raise NotImplementedError
        return algorithms.nlargest_dict(number, self.__resource, idx)

    def get(self, resource, feature):
        if feature == self.COUNT:
            idx = self.__count_index 
        elif feature == self.BANDWIDTH:
            idx = self.__bandwidth_index
        elif feature == self.SIZE:
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


    def test_update_resource(self):
        resources = ResourceStatistics()
        for entry in self.data:
            resources.update(entry)
        print "A count: ", resources.get("A", resources.COUNT)
        print "A size: ", resources.get("A", resources.SIZE)
        print "A bandwidth: ", resources.get("A", resources.BANDWIDTH)

    def test_find_large_resources(self):
        resources = ResourceStatistics()
        for entry in self.data:
            resources.update(entry)
        print resources.top(2, resources.COUNT)
        print resources.top(2, resources.BANDWIDTH)

if __name__ == '__main__':
        unittest.main()
