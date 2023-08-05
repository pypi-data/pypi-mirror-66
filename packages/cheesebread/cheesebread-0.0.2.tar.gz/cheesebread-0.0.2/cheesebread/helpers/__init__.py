#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce

from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def _get_date_list(start, end, months=1, **kwargs):
    """
    Create list of dates

    :param start: start. Expected format %Y-%m-%d    
    :param end: end. Expected format %Y-%m-%d  
    """
    start = datetime.strptime(start, '%Y-%m-%d')#.replace(tzinfo=timezone.utc)
    end = datetime.strptime(end, '%Y-%m-%d')#.replace(tzinfo=timezone.utc)

    while start <= end:
        yield start
        start += relativedelta(months=months, **kwargs)

def get_date_pairs(start, end, **kwargs):
    """
    Create list of date pairs
  
    :param start: start. Expected format %Y-%m-%d    
    :param end: end. Expected format %Y-%m-%d  
    """
    li = list(_get_date_list(start, end, **kwargs))
    return zip(li, li[1:])

def get_timestamp_pairs(start, end):
    """
    Create list of timestamp pairs
    
    :param start: start. Expected format %Y-%m-%d    
    :param end: end. Expected format %Y-%m-%d  
    """
    li = list(map(lambda x : int(datetime.timestamp(x)), _get_date_list(start, end, months=0, days=1)))
    return zip(li, li[1:])

def _get_ticks(start, end, ticks):
    diff = (end  - start ) / ticks
    for i in range(ticks):
        yield (start + diff * i)
    yield end

def get_timestamp_ticks(start, end, ticks):
    """
    Create list of timestamp pairs
    
    :param start: start. Expected format %Y-%m-%d    
    :param end: end. Expected format %Y-%m-%d  
    """
    # create ticks
    li = [list(_get_ticks(i, j, ticks)) for i, j in get_date_pairs(start, end)]

    # flatten list
    li = reduce(lambda x,y:x+y, li)
    
    # map timestamp
    li = list(map(datetime.timestamp, li))

    return zip(li, li[1:])