#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
import unittest
import algorithms

class ResourceStatistics(object):
    def __init__(self):
        self.count = 0
        self.size = 1
        self.bandwidth = 2
        
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
                    /float(self.__resource[res][self.__count_index])
            else:
                self.__resource[res] =  [0, 0, 0]
                self.__resource[res][self.__count_index] = 1 
                self.__resource[res][self.__size_index] = float(entry["Size"])
                self.__resource[res][self.__bandwidth_index] = entry["Size"]

    def top(self, number, feature):
        if feature == self.count:
            idx = self.__count_index 
        elif feature == self.bandwidth:
            idx = self.__bandwidth_index
        elif feature == self.size:
            idx = self.__size_index
        else:
            raise NotImplementedError
        keys, values = algorithms.nlargest_dict(number, self.__resource, idx)
        return zip(values, keys)

    def get(self, resource, feature):
        if feature == self.count:
            idx = self.__count_index 
        elif feature == self.bandwidth:
            idx = self.__bandwidth_index
        elif feature == self.size:
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
        self.assertEqual(resources.get("A", resources.count), 3)
        self.assertEqual(resources.get("A", resources.size), 5.0/3)
        self.assertEqual(resources.get("A", resources.bandwidth), 5)

    def test_find_large_resources(self):
        resources = ResourceStatistics()
        for entry in self.data:
            resources.update(entry)
        top = resources.top(2, resources.count)
        self.assertEqual(top[0], (3, "A")) 
        self.assertEqual(top[1], (2, "C")) 

        top = resources.top(2, resources.bandwidth)
        self.assertEqual(top[0], (33, "E")) 
        self.assertEqual(top[1], (23, "B")) 

        top = resources.top(2, resources.size)
        self.assertEqual(top[0], (33, "E")) 
        self.assertEqual(top[1], (11.5, "B")) 

if __name__ == '__main__':
        unittest.main()
