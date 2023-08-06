#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
time_lib

measuring time with a stack of time points
and a converter of seconds to time string

author: Marek Ryćko

25.04.2008

temporarily added functions time_b, time_e
later move them to another location
25.09.2008

converted to python3
21.02.2019 03:15:42

using stack of time points
19.03.2019 02:08:36
'''

# used by time_b, time_e
import time

# ------------------------------------------------------------------------------
# string time operations:
# ------------------------------------------------------------------------------

def declension(n, root):
    '''
    return a form of a unit of measure root
    with a declension according to the number n >= 0
    declension(1, 'kilogram') --> '1 kilogram'
    declension(2, 'kilogram') --> '2 kilograms'
    '''
    suffix = '' if n == 1 else 's'
    return ('%d ' + root + suffix) % n

def time_str(sec, scale=6):
    '''
    return a time string, constructed from some seconds (incl. fractional part)
    scale digits in decimal part
    sec >= 0
    '''
    minutes, sec = divmod(sec, 60)
    #~ print(minutes, sec)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    # collecting the result string:
    l = []
    if days > 0: l.append(declension(days, 'day'))
    if hours > 0: l.append(declension(hours, 'hour'))
    if minutes > 0: l.append(declension(minutes, 'minute'))
    #~ if sec > 0:
    if isinstance(sec, float):
        l.append(('%2.'+str(scale)+'f seconds') % sec)
    else:
        l.append(declension(sec, 'second'))
    # construct the string:
    s = ', '.join(l)
    return s

# ------------------------------------------------------------------------------
# time points stack operations:
# ------------------------------------------------------------------------------

time_stack = []

def time_b():
    time_stack.append(time.time())

def till_now():
    time_start = time_stack.pop()
    time_now = time.time()
    time_dist = time_now - time_start
    return time_dist
    
def time_e():
    '''
    calculate the time distance popping up fromt the time stack
    and return the time in the form of time string in Egnlish
    '''
    # ~ result = "Time elapsed = " + time_str(till_now())
    result = time_str(till_now())
    return result
    
if __name__ == "__main__":
    
    # test of time string:

    print(declension(0, 'day'))
    print(declension(1, 'day'))
    print(declension(2, 'day'))

    print(time_str(0))
    print(time_str(1))
    print(time_str(2))
    print(time_str(0.123456))
    print(time_str(123.123456))
    print(time_str(6723.123456))
    print(time_str(696723.123456))
    print(time_str(96723.123456))
