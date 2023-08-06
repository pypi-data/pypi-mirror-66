#!/usr/bin/python3
# -*- coding: utf-8 -*-

# author: Marek Ryćko
__author__ = 'Marek Ryćko <marek@do.com.pl>'

'''
run library run_lib
executing major steps by runnig an external program

15.03.2019 14:54:08
start
by transferring a metapost running part
from mp_to_eps_oti
'''



# standard library
# ~ import re
# at least for os.path.join:
import os
# ~ import shutil
import subprocess   

# modules of Algotype:
import algotype.at_lib as lib
# log_lib used for time distance printing
import algotype.log_lib as log_lib

# modules from MR library:
import algotype.time_lib as time_lib

generating_eps = 'eps'
generating_tfm = 'tfm'

def mp(conf, fb, generating):
    '''
    run metapost according to the configuration
    in particular in conf['mp_root_dir']
    applying it (the metapost) to the file of the “bare” filename fb
    
    genarating is a parameter (int or string) given to the metapost as:
        \generating:=0
    or:
        \generating:=1
    '''
    
    # ------------------------------------------------------------------------------
    # in TeXLive installation engine names are to be in proper system paths:


    # collecting command line:
    cl = [conf['metapost_engine']]

    if 'mp_interaction' in conf:
        # interaction defined in config; we put it to the command line arguments:
        cl.append('-interaction=' + conf['mp_interaction'])

    if 'mp_recorder' in conf and conf['mp_recorder']:
        # 'recorder' defined and true:
        cl.append('-recorder')
        
    # standard output type, by default: screen
    standard_output_type = 'screen'
    if 'mp_standard_output' in conf:
        standard_output_type = conf['mp_standard_output']
        if standard_output_type == 'file':
            standard_output = os.path.join(conf['mp_root_dir'], fb + r'.out')
        elif standard_output_type == 'devnull':
            standard_output = os.devnull
        if standard_output_type != 'screen':
            standard_output_handle = open(standard_output, 'w')

    if generating == 'eps':
        generating_n = 0
    elif generating == 'tfm':
        generating_n = 1
    else:
        # this should not happen
        pass
    
    generating_string = r'\generating:=%s;' % str(generating_n)

    mp_path = os.path.join(conf['mp_root_dir'], fb + r'.mp')
    cl.extend([generating_string, r'\input ' + mp_path])

    # to do: with --recorder:
    #$engine --recorder $fb \\generating:=0\; \\input $fb.mp

    # save and change directory:
    lib.dir_save()
    lib.dir_change(conf['mp_root_dir'])

    # make the run, measuring time:
    time_lib.time_b()
    if standard_output_type == 'screen':
        subprocess.run(cl)
    else:
        subprocess.run(cl, stdout=standard_output_handle)
    log_lib.debug(time_lib.time_e())

    # restore the current directory:
    lib.dir_restore()