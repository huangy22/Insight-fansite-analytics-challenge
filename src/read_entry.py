#import numpy as np
import re
import datetime as dt
from dateutil.parser import parse
import unittest

# Regex for the Apache common log format.
parts = [
            r'(?P<Host>\S+)',                   # host %h
            r'\S+',                             # indent %l (unused)
            r'(?P<User>\S+)',                   # user %u
            r'\[(?P<Time>.+)\]',                # time %t
            r'"(?P<Request>.*)"',               # request "%r"
            r'(?P<Status>[0-9]+)',              # status %>s
            r'(?P<Size>\S+)',                   # size %b (careful, can be '-')
    ]

pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

DF_FORMAT = "[%d/%b/%Y:%H:%M:%S"

month_map = {'Jan': 1, 'Feb': 2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 
            'Aug':8,  'Sep': 9, 'Oct':10, 'Nov': 11, 'Dec': 12}

def apachetime(s):
    global month_map
    return dt.datetime(int(s[7:11]), month_map[s[3:6]], int(s[0:2]), \
            int(s[12:14]), int(s[15:17]), int(s[18:20]))

# Change Apache log items into Python types.
def pythonized(d):
    # Clean up the request.
    request_list = d["Request"].split()
    if len(request_list) > 1:
        d["Request_Type"] = request_list[0]
        d["Request"] = request_list[1]
    else:
        d["Request_Type"] = None

    # Some dashes become None.
    if d["User"] == "-":
        d["User"] = None

    # The size dash becomes 0.
    if d["Size"] == "-":
        d["Size"] = 0
    else:
        d["Size"] = int(d["Size"])

    # The status dash becomes 0.
    if d["Status"] == "-":
        d["Status"] = 0
    else:
        d["Status"] = int(d["Status"])

    # Convert the timestamp into a datetime object. Accept the server's time zone.
    time, zone = d["Time"].split()
    d["Time"] = apachetime(time)
    d["TimeZone"] = zone
    return d

def read_entry(line):
    m = pattern.match(line)
    hit = m.groupdict()
    return pythonized(hit)

class TestFileReadInMethods(unittest.TestCase):
    def setUp(self):
        self.file = ['199.72.81.55 - - [01/Jul/1995:00:00:01 -0000] "POST /login HTTP/1.0" 401 -',
                     '220.149.67.62 - - [01/Sep/1995:00:00:27 -0000] "GET /images/KSC-logosmall.gif HTTP/1.0" 200 1204']

    def test_read_entry(self):
        entry_dict = read_entry(self.file[0])
        self.assertEqual(entry_dict["Host"], "199.72.81.55")
        self.assertEqual(entry_dict["Time"], dt.datetime.strptime('[01/Jul/1995:00:00:01', DF_FORMAT))
        self.assertEqual(entry_dict["Request_Type"], "POST")
        self.assertEqual(entry_dict["Request"], "/login")
        self.assertEqual(entry_dict["Status"], 401)
        self.assertEqual(entry_dict["Size"], 0)

        entry_dict = read_entry(self.file[1])
        self.assertEqual(entry_dict["Host"], "220.149.67.62")
        self.assertEqual(entry_dict["Time"], dt.datetime.strptime('[01/Sep/1995:00:00:27', DF_FORMAT))
        self.assertEqual(entry_dict["Request_Type"], "GET")
        self.assertEqual(entry_dict["Request"], "/images/KSC-logosmall.gif")
        self.assertEqual(entry_dict["Status"], 200)
        self.assertEqual(entry_dict["Size"], 1204)


if __name__ == '__main__':
        unittest.main()
