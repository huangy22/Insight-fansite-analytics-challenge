#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 

import re
import sys
import json
from urllib2 import urlopen
import utility
import traceback
    
def is_valid_ip(ip):
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        return False # one of the 'parts' not convertible to integer
    except (AttributeError, TypeError):
        return False # `ip` isn't even a string


infile = sys.argv[1]
outdir = sys.argv[2]

log = utility.Logger("./")

country = {}
total = 0.0

with open(infile, 'r') as reader:
    for line in reader: 
        line = line.rstrip()
        if is_valid_ip(line):
            try:
                url = 'http://ipinfo.io/'+line+'/json'
                response = urlopen(url, timeout=1)
                data = json.load(response)

                #IP=data['ip']
                #org=data['org']

                city = data['city']
                region=data['region']

                if data['country'] in country:
                    country[data['country']] += 1
                else:
                    country[data['country']] = 1
                total += 1.0
            except:
                log.warning("The extraction of geolocation fails.\n{0}".format(traceback.format_exc()))

with open(outdir + "country.csv", "w") as writer:
    writer.write("Country, Proportion of Users\n")
    for key in country.keys():
        writer.write(key.encode("ascii", "ignore") + ", " +
                     str(country[key]/total) + "\n")
