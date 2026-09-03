#!/usr/bin/env python
"""URLmapper.py"""
import sys
import re

# regex to find href="..." patterns and capture the URL inside the quotes
url_pattern = re.compile(r'href="([^"]*)"')

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # find all URLs on this line
    urls = url_pattern.findall(line)
    # increase counters
    for url in urls:
        # tab-delimited; each URL occurrence counts as 1
        print('%s\t%s' % (url, 1))
