#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the function to find n largest attributes in dictionary according to
a specified attribute.
Author: Yuan Huang
"""
import unittest
import heapq

def nlargest_dict(n_top, dictionary, axis):
    """
    Find n largest entries in a dictionary, the sort axis is specified as axis.
    Args:
        n_top(int): the number of top entries
        dict(dict): the data in dictionary
        axis(int): the index to sort.
    Returns:
        top_keys(list): The top n keys in a list.
        top_values(list): The top n values in a list.
    """
    top_keys = heapq.nlargest(n_top, dictionary, key = lambda x: dictionary[x][axis])
    return  top_keys, [dictionary[key][axis] for key in top_keys]

def nsmallest_dict(n_bottom, dictionary, axis):
    """
    Find n smallest entries in a dictionary, the sort axis is specified as axis.
    Args:
        n_bottom(int): the number of least entries
        dict(dict): the data in dictionary
        axis(int): the index to sort.
    Returns:
        bottom_keys(list): The n keys at the bottom in a list.
        bottom_values(list): The n values at the bottom in a list.
    """
    bottom_keys = heapq.nsmallest(n_bottom, dictionary, key=lambda x: (dictionary[x][axis], x))
    return  bottom_keys, [dictionary[key][axis] for key in bottom_keys]

class TestAlgorithms(unittest.TestCase):
    """The unittest class for nlargest_dict and linked list."""
    def setUp(self):
        """Set up for the test cases."""
        self.dict = {"A": [15, 300], "B":[15, 200], "C": [1, 3000]}

    def test_nlargest_dict(self):
        """Test for the nlargest functionality for a dictionary."""
        keys, values = nlargest_dict(2, self.dict, 0)
        self.assertEqual(keys[0], "A")
        self.assertEqual(values[0], 15)
        self.assertEqual(keys[1], "B")
        self.assertEqual(values[1], 15)

        keys, values = nlargest_dict(2, self.dict, 1)
        self.assertEqual(keys[0], "C")
        self.assertEqual(values[0], 3000)
        self.assertEqual(keys[1], "A")
        self.assertEqual(values[1], 300)

    def test_nsmallest_dict(self):
        """Test for the nsmallest functionality for a dictionary."""
        keys, values = nsmallest_dict(2, self.dict, 0)
        self.assertEqual(keys[0], "C")
        self.assertEqual(values[0], 1)
        self.assertEqual(keys[1], "A")
        self.assertEqual(values[1], 15)

        keys, values = nsmallest_dict(2, self.dict, 1)
        self.assertEqual(keys[0], "B")
        self.assertEqual(values[0], 200)
        self.assertEqual(keys[1], "A")
        self.assertEqual(values[1], 300)

if __name__ == '__main__':
    unittest.main()
