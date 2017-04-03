#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Provide the class to read in a line in the log file and transfer it
into a dictionary.
Author: Yuan Huang
"""
import re
import datetime as dt
import unittest

# Regex for the Apache common log format.
PARTS = [r'(?P<Host>\S+)',                   # host %h
         r'\S+',                             # indent %l (unused)
         r'(?P<User>\S+)',                   # user %u
         r'\[(?P<Time>.+)\]',                # time %t
         r'"(?P<Request>.*)"',               # request "%r"
         r'(?P<Status>[0-9]+)',              # status %>s
         r'(?P<Size>\S+)',                   # size %b (careful, can be '-')
        ]

PATTERN = re.compile(r'\s+'.join(PARTS)+r'\s*\Z')

DF_FORMAT = "[%d/%b/%Y:%H:%M:%S"

MONTH_MAP = {'Jan': 1, 'Feb': 2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7,
             'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

def apachetime(tstr):
    return dt.datetime(int(tstr[7:11]), MONTH_MAP[tstr[3:6]], int(tstr[0:2]),
                       int(tstr[12:14]), int(tstr[15:17]), int(tstr[18:20]))

# Change Apache log items into Python types.
def pythonized(entry_dict):
    # Clean up the request.
    request_list = entry_dict["Request"].split()

    if request_list[0] in ["GET", "POST", "HEAD"]:
        entry_dict["Request_Type"] = request_list[0]
        entry_dict["Request"] = request_list[1]
    else:
        entry_dict["Request_Type"] = None
        raise TypeError("Type of request is not found in the entry: {0}".format(entry_dict["Request"]))

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
    time, zone = entry_dict["Time"].split()
    entry_dict["Time"] = apachetime(time)
    entry_dict["TimeZone"] = zone
    return entry_dict

def read_entry(line):
    matches = PATTERN.match(line)
    if matches is None:
        raise TypeError("No pattern is found in line {0}".format(line))
    hit = matches.groupdict()
    dictionary = pythonized(hit)
    return dictionary

class TestFileReadInMethods(unittest.TestCase):
    def setUp(self):
        self.file = ['199.72.81.55 - - [01/Jul/1995:00:00:01 -0000] "POST /login HTTP/1.0" 401 -',
                     '220.149.67.62 - - [01/Sep/1995:00:00:27 -0000] "GET \
                     /images/KSC-logosmall.gif HTTP/1.0" 200 1204']

    def test_read_entry(self):
        entry_dict = read_entry(self.file[0])
        self.assertEqual(entry_dict["Host"], "199.72.81.55")
        self.assertEqual(entry_dict["Time"], dt.datetime.strptime('[01/Jul/1995:00:00:01',
                                                                  DF_FORMAT))
        self.assertEqual(entry_dict["Request_Type"], "POST")
        self.assertEqual(entry_dict["Request"], "/login")
        self.assertEqual(entry_dict["Status"], 401)
        self.assertEqual(entry_dict["Size"], 0)

        entry_dict = read_entry(self.file[1])
        self.assertEqual(entry_dict["Host"], "220.149.67.62")
        self.assertEqual(entry_dict["Time"], dt.datetime.strptime('[01/Sep/1995:00:00:27',
                                                                  DF_FORMAT))
        self.assertEqual(entry_dict["Request_Type"], "GET")
        self.assertEqual(entry_dict["Request"], "/images/KSC-logosmall.gif")
        self.assertEqual(entry_dict["Status"], 200)
        self.assertEqual(entry_dict["Size"], 1204)


if __name__ == '__main__':
    unittest.main()
