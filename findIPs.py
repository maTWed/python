#!/usr/bin/python3
# findIPs.py: Takes a file as input and scrapes it for IP Addresses
# ie: cat /var/log/syslog | ./findIPs.py

__author__ = "maTWed"

import fileinput
import re
from collections import Counter

mylist = []

for line in fileinput.input():
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
    if ip:
        for i in ip:
            mylist.append(i)

print(Counter(mylist))