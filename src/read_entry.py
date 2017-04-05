#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to read in a line in the log file and transfer it
into a dictionary.
Author: Yuan Huang
"""
import re
import unittest
import datetime as dt
from dateutil import parser

# Regex for the Apache common log format.
PARTS = [r'(?P<Host>\S+)',                   # host %h
         r'\S+',                             # indent %l (unused)
         r'(?P<User>\S+)',                   # user %u
         r'\[(?P<Time>.+)\]',                # time %t
         r'(?P<Request>.*)',                 # request "%r"
         r'(?P<Status>[0-9]+)',              # status %>s
         r'(?P<Size>\S+)',                   # size %b (careful, can be '-')
        ]

# The pattern for the Apache log
PATTERN = re.compile(r'\s+'.join(PARTS)+r'\s*\Z')

# The map between the name of month and its number
MONTH_MAP = {'Jan': 1, 'Feb': 2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7,
             'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

class FixOffset(dt.tzinfo):
    """
    Fixed offset in minutes east from UTC.
    Inherited from dt.tzinfo.
    """

    def __init__(self, string):
        if string[0] == '-':
            direction = -1
            string = string[1:]
        elif string[0] == '+':
            direction = +1
            string = string[1:]
        else:
            direction = +1
            string = string

        hr_offset = int(string[0:2], 10)
        min_offset = int(string[2:3], 10)
        min_offset = hr_offset * 60 + min_offset
        min_offset = direction * min_offset

        self.__offset = dt.timedelta(minutes=min_offset)

        self.__name = string

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return self.__offset

    def __repr__(self):
        return repr(self.__name)

def __apachetime(tstr):
    """
    Transform the time string in Apache time format (without timezone information)
    into datetime object.
    Args:
        tstr(str): time string in format '%d/%b/%Y:%H:%M:%S', e.g. "01/Jul/1997:00:00:01"
    Returns:
        datetime object.
    """
    tz = FixOffset(tstr[21:26])
    return dt.datetime(int(tstr[7:11]), MONTH_MAP[tstr[3:6]], int(tstr[0:2]),
                       int(tstr[12:14]), int(tstr[15:17]), int(tstr[18:20]), tzinfo=tz)

def __format_standardize(entry_dict):
    """
    Change the format and datatype of the Apache log dictionary.
    Args:
        entry_dict(dict): the groupdict result of pattern matches in a Apache log item.
    Returns:
        dictionary:
            Request is seperated into Request_Type(GET,POST,HEAD)
            and Request(The name of resource). '-' is turned into None (in User)
            or 0 (in Size and Status). Time is transferred into a datetime object.
    """
    # Clean up the request.
    request_list = entry_dict["Request"].split()
    entry_dict["Request_Type"] = None

    if len(request_list) >= 2:
        entry_dict["Request"] = request_list[1]
        request_list[0] = (request_list[0].decode('utf-8').strip())[1:]
        if request_list[0] in ["GET", "POST", "HEAD"]:
            entry_dict["Request_Type"] = request_list[0]
        else:
            raise TypeError("Request Type is not GET/POST/HEAD in the entry: {0}".format(entry_dict["Request_Type"]))
    else:
        raise TypeError("Request format is not correct in the entry: {0}".format(entry_dict["Request"]))

    # Some dashes become None.
    if entry_dict["User"] == "-":
        entry_dict["User"] = None

    # The size dash becomes 0.
    if entry_dict["Size"] == "-":
        entry_dict["Size"] = 0
    else:
        entry_dict["Size"] = int(entry_dict["Size"])

    # The status dash becomes 0.
    if entry_dict["Status"] == "-":
        entry_dict["Status"] = 0
    else:
        entry_dict["Status"] = int(entry_dict["Status"])

    # Convert the timestamp into a datetime object. Accept the server's time zone.
    entry_dict["Time"] = __apachetime(entry_dict["Time"])
    return entry_dict

def read_entry(line):
    """
    Transform a line in the log file into a dictionary with standardized format.
    Args:
        line(str): a string with Apache log format, e.g. '199.72.81.55 - -
        [01/Jul/1995:00:00:01 -0000] "POST /login HTTP/1.0" 401 -'.
    Returns:
        dictionary:
            A dictionary with keys "Host"(str), "User"(str), "Time"(datetime),
            "Request_Type"(str, GET/POST/HEAD), "Request"(str), "Status"(int), "Size"(int)
    """

    # Use regular expression to find the patterns in the log string
    matches = PATTERN.match(line)
    if matches is None:
        raise TypeError("No pattern is found in line {0}".format(line))

    # Get the dictionary of the log with all the matched patterns
    hit = matches.groupdict()

    # Change the format of the dictionary
    dictionary = __format_standardize(hit)
    return dictionary

class TestReadEntry(unittest.TestCase):
    """
    Unittest Class for the read_entry function.
    """
    def setUp(self):
        """
        Set up two lines of Apache log.
        """
        self.file = ['199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "POST /login HTTP/1.0" 401 -',
                     '220.149.67.62 - - [01/Sep/1995:00:00:27 -0400] "GET \
                     /images/KSC-logosmall.gif HTTP/1.0" 200 1204']

    def test_read_entry(self):
        """
        Test the key and values in the returned dictionary for the examples.
        """
        entry_dict = read_entry(self.file[0])
        self.assertEqual(entry_dict["Host"], "199.72.81.55")
        self.assertEqual(entry_dict["Time"], parser.parse("01 Jul 1995 00:00:01 -0400"))
        self.assertEqual(entry_dict["Request_Type"], "POST")
        self.assertEqual(entry_dict["Request"], "/login")
        self.assertEqual(entry_dict["Status"], 401)
        self.assertEqual(entry_dict["Size"], 0)

        entry_dict = read_entry(self.file[1])
        self.assertEqual(entry_dict["Host"], "220.149.67.62")
        self.assertEqual(entry_dict["Request_Type"], "GET")
        self.assertEqual(entry_dict["Request"], "/images/KSC-logosmall.gif")
        self.assertEqual(entry_dict["Status"], 200)
        self.assertEqual(entry_dict["Size"], 1204)

if __name__ == '__main__':
    unittest.main()
