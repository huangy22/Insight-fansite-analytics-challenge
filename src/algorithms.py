#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 

import unittest
import heapq


def nlargest_dict(n, dictionary, axis):
    """Find n largest entries in a dictionary, the sort axis is specified as axis.
    Args:
        n(int): the number of top entries
        dict(dict): the data in dictionary
        axis(int): the index to sort.
    Returns:
        top_keys(list): The top n keys in a list.
        top_values(list): The top n values in a list.
    """
    top_keys = heapq.nlargest(n, dictionary, key=lambda x: dictionary[x][axis])
    return  top_keys, [dictionary[key][axis] for key in top_keys]

# Node class 
class Node:
    # Constructor to initialize the node object
    def __init__(self, data):
        self.data = data
        self.next = None
 
class LinkedList:
    # Function to initialize head
    def __init__(self, length):
        self.head = None
        self.length = 0
        self.max_length = length
 
    def sorted_insert_data(self, new_data):
        new_node = Node(new_data)
        # Special case for the empty linked list 
        if self.head is None:
            new_node.next = self.head
            self.head = new_node
 
        # Special case for head at end
        elif self.head.data >= new_node.data:
            new_node.next = self.head
            self.head = new_node
 
        else :
            # Locate the node before the point of insertion
            current = self.head
            while(current.next is not None and current.next.data < new_node.data):
                current = current.next
             
            new_node.next = current.next
            current.next = new_node
        self.length += 1
        if self.length > self.max_length:
            self.remove(self.head)
        return new_node

    def sorted_insert_node(self, new_node):
        # Special case for the empty linked list 
        if self.head is None:
            new_node.next = self.head
            self.head = new_node
 
        # Special case for head at end
        elif self.head.data >= new_node.data:
            new_node.next = self.head
            self.head = new_node
 
        else :
            # Locate the node before the point of insertion
            current = self.head
            while(current.next is not None and current.next.data < new_node.data):
                current = current.next
             
            new_node.next = current.next
            current.next = new_node

        self.length += 1
        if self.length > self.max_length:
            self.remove(self.head)
        return new_node

    def remove(self, node):
        current = self.head
        prev = None
        while current is not node and current is not None:
            prev = current
            current = current.next
        if prev is not None:
            prev.next = node.next
        else:
            self.head = node.next
        self.length -= 1

    def replace_data(self, node, new_data):
        node.data = new_data

    def sort_node(self, node_to_sort):
        self.remove(node_to_sort)
        node_to_sort = self.sorted_insert_node(node_to_sort)
        return node_to_sort

    def min(self):
        return self.head.data

    def get_list(self):
        data_list = []
        current = self.head
        while current is not None:
            data_list.append(current.data)
            current = current.next
        return data_list
            
class TestHost(unittest.TestCase):
    def setUp(self):
        self.dict = {"A": [15, 300], "B":[15, 200], "C": [1, 3000]}

    def test_nlargest_dict(self):
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

    def test_linked_list(self):
        mylist = LinkedList(10)

        last = mylist.sorted_insert_data(5)
        last = mylist.sorted_insert_data(1)
        last = mylist.sorted_insert_data(3)
        last = mylist.sorted_insert_data(2)
        last = mylist.sorted_insert_data(15)
        last = mylist.sorted_insert_data(12)
        last = mylist.sorted_insert_data(32)
        last = mylist.sorted_insert_data(24)
        last = mylist.sorted_insert_data(41)
        last = mylist.sorted_insert_data(4)
        last = mylist.sorted_insert_data(2)

        mylist.replace_data(last, 44)
        mylist.sort_node(last)

        res = mylist.get_list()
        print res

if __name__ == '__main__':
        unittest.main()
