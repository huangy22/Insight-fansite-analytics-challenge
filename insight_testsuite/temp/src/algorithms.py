#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide find n largest attributes in dictionary and sorted linked list operations.
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
    top_keys = heapq.nlargest(n_top, dictionary, key=lambda x: dictionary[x][axis])
    return  top_keys, [dictionary[key][axis] for key in top_keys]

class Node:
    """The Node class with pointer "next" and "data"."""

    def __init__(self, data):
        """Initialize a node with data.
        Args:
            data(any object): the data of the new node.
        """
        self.data = data
        self.next = None

    def replace_data(self, new_data):
        """Replace the data on a node.
        Args:
            new_data(data object): new data to put in node.
        """
        self.data = new_data


class LinkedList:
    """LinkedList class: a ascending ordered linked list with a maximum length."""

    def __init__(self, max_length):
        """Initialize a linked list with fixed length.
        Args:
            length(int): the fixed maximum length of the linked list.
        """
        self.head = None
        self.length = 0
        self.max_length = max_length

    def sorted_insert_data(self, new_data):
        """Insert a new data into the sorted linked list.
        The linked list is already in increasing order.
        Args:
            new_data(data object): the data of the new node that needs to be inserted.
        Returns:
            new_node(Node): the new node in the list, the linked list remains sorted
            after the insertion.
        """
        new_node = Node(new_data)
        self.sorted_insert_node(new_node)
        return new_node

    def sorted_insert_node(self, new_node):
        """Insert a new node into the sorted linked list.
        The linked list is already in increasing order.
        Args:
            new_node(Node): the new node needs to be inserted.
        Returns:
            new_node(Node): the node in the list, the linked list remains sorted
            after the insertion.
        """
        # Special case for the empty linked list
        if self.head is None:
            new_node.next = self.head
            self.head = new_node

        # Special case for head at end
        elif self.head.data >= new_node.data:
            new_node.next = self.head
            self.head = new_node

        else:
            # Locate the node before the point of insertion
            current = self.head
            while current.next is not None and current.next.data < new_node.data:
                current = current.next

            new_node.next = current.next
            current.next = new_node

        # Increase the length of the linked list by 1.
        self.length += 1
        # When the length exceeds the maximum length, remove the node with smallest value (head).
        if self.length > self.max_length:
            self.remove(self.head)
        return new_node

    def remove(self, node):
        """Remove a node in the linked list.
        Args:
            node(Node): The node to be removed.
        """
        # Locate the node before the node that needs to be removed.
        current = self.head
        prev = None
        while current is not node and current is not None:
            prev = current
            current = current.next

        # Remove the node and assign its next to prev.next
        if prev is not None:
            prev.next = node.next
        else:
            # Special case when the node to be removed is the head
            self.head = node.next

        # Decrease the length of the linked list by 1.
        self.length -= 1

    def sort_node(self, node_to_sort):
        """Put one node in the right place of the sorted linked list (except for this one node).
        The current linked list is in sorted order except for one node: node_to_sort. This function
        put this node in the right place without changing the relative positions of other nodes.
        Args:
            node_to_sort(Node): the node that needs to be sorted.
        Returns:
            node_to_sort(Node): the node in the right position.
        """
        # Remove the node to be sorted, the linked list becomes a sorted list with n-1 nodes.
        self.remove(node_to_sort)
        # Insert the node into the sorted linked list in its right position.
        node_to_sort = self.sorted_insert_node(node_to_sort)
        return node_to_sort

    def min(self):
        """Get the minimum value of the linked list.
        Returns:
            minimum_data(data object): the data of the head node (the linked list is in
            ascending order).
        """
        return self.head.data

    def get_list(self, order="ascend"):
        """Get a list of data in the linked list in ascending order.
        Returns:
            return_list(list): a list of all data in each nodes of the linked list, the list is
            ordered according to its data values.
        """
        data_list = []
        current = self.head
        while current is not None:
            data_list.append(current.data)
            current = current.next
        return_list = data_list
        if order == "descend":
            return_list = []
            for i in range(len(data_list))[::-1]:
                return_list.append(data_list[i])
        return return_list

class TestAlgorithms(unittest.TestCase):
    """The unittest class for nlargest_dict and linked list."""
    def setUp(self):
        """Set up for the test cases."""
        self.dict = {"A": [15, 300], "B":[15, 200], "C": [1, 3000]}
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
        self.linkedlist = mylist
        self.lastnode = last


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

    def test_linked_list(self):
        """Test for replace data to a node and reinsert it in linked list."""
        self.lastnode.replace_data(44)
        self.linkedlist.sort_node(self.lastnode)

        res = self.linkedlist.get_list()
        print res

if __name__ == '__main__':
    unittest.main()
