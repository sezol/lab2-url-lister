#!/usr/bin/env python
"""URLreducer.py"""
from operator import itemgetter
import sys

current_url = None
current_count = 0
url = None

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    url, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: url) before it is passed to the reducer
    if current_url == url:
        current_count += count
    else:
        if current_url and current_count > 5:
            # only output URLs with more than 5 references
            print('%s\t%s' % (current_url, current_count))
        current_count = count
        current_url = url

# do not forget to output the last url if needed!
if current_url == url and current_count > 5:
    print('%s\t%s' % (current_url, current_count))

