#!/usr/bin/python3
# -*- coding: utf-8 -*-

# make the file both Python 2 and Python 3 compatible
# probably not needed any more, as of 16.03.2020 20:07:02:
# ~ from __future__ import print_function

# author: Marek Ryćko
__author__ = 'Marek Ryćko <marek@do.com.pl>'

'''
config
paths, filenames and other variables/attributes/parameters
for the Algotype font generating system

intended to be both python2 and python3 compatible
(at least as long as it is needed; some components still use Python 2)

18.02.2019 02:07:39
start, as:
config
paths and filenames
for the Metatype1 font generating system


28.06.2019 00:36:06
name of the system changed to Algotype
'''

# ------------------------------------------------------------------------------
# for calculatig paths:
import os
# for error messages and breaking the program execution
import sys

# Algotype modules:
from . import at_lib as lib
# prints converted to log_lib function calls:
from . import log_lib

# ------------------------------------------------------------------------------
# installation config:
# ------------------------------------------------------------------------------

import algotype.config_interpreter as ci
import algotype.parse_config as parse_config
    
def dict_repr(j):
    sl = []
    for k, v in j.items():
        sl.append('%s: %s' % (k, repr(v)))
    s = '\n'.join(sl)
    return s

def prepare(configs):
    '''
    read a series of config files
    and prepare a config structure as a parsed concatenation
    of the files
    '''
    log_lib.debug_separator(element='-')
    log_lib.debug(f"{'-' * 30} config analysis:")
    # prepare the input string as a concatenation of config files:
    
    # first read input file strings (as sl — string list):
    sl = []
    for co in configs:
        # co is a filename of a config file
        try:
            with lib.open_r(co) as fh:
                s = fh.read()
                sl.append(s)
        except IOError as e:
            log_lib.critical(f"input error ({e.errno}) reading config file {co}: {e.strerror}")
        except:
            # handle other exceptions such as attribute errors:
            log_lib.critical(f"error reading config file {co}")
    
    config_sum = '\n'.join(sl)
    
    # parse the combined config string (without interpretation):
    inp_sum = parse_config.parse(config_sum)

    log_lib.debug(f"parsed config before intepreting the “programs” (right hand side expressions):")
    log_lib.debug(dict_repr(inp_sum))

    result_sum = ci.translate_dict(inp_sum)
    
    return result_sum



if __name__ == '__main__':
    import json
    prepare()
    s2 = json.dumps(run, indent=4, ensure_ascii=False) 
    log_lib.info(s2)
