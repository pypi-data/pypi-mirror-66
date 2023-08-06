#!/usr/bin/python3
# -*- coding: utf-8 -*-

# make the file both Python 2 and Python 3 compatible
from __future__ import print_function

'''
A library of functions for logging events (collecting
and writing them to the screen and to log file/s).

'''

__author__ = "Marek Ryćko"
__copyright__ = "Copyright (c) 2019 by Marek Ryćko"
__version__ = "0.1"
__maintainer__ = "Marek Ryćko"
__email__ = "marek@do.com.pl"
__status__ = "Alpha"



# standard library:
import logging
# sys.exit, sys.version_info:
import sys
# file removal:
import os
# date/time stamps:
import datetime
# wrapping test:
import textwrap
# io file reading and writing for compatibility with both Python 2 and Python 3:
import io


# Algotype library:
# none

# ------------------------------------------------------------------------------

    




# ------------------------------------------------------------------------------
class Log_machinery:
    '''
    The machinery of logging, working only in Python >= 2.6.
    
    (since Python 2.6 the io.open is upward compatible with Python 3)
    '''
    
    def __init__(self, path=None, debug_path=None, remove=False,
            encoding=None):
        self.log_path = path
        if debug_path is None:
            self.debug_path = path
        else:
            self.debug_path = debug_path
            
        # ensure the Python version is supported, before any further actions:
        self.check_python_version()
        
        # if removing, first remove:
        if remove:
            self.log_file_remove()
            self.debug_file_remove()
            
        if encoding is None:
            self.encoding = 'utf-8'
        else:
            self.encoding = encoding
        
        self.log_file_open()
        self.debug_file_open()
        self.level = 'info'
        
        self.last_datetime_string = None
        
    def check_python_version(self):
        
        major = sys.version_info.major
        minor = sys.version_info.minor
        micro = sys.version_info.micro
        
        # some files are Python-version-dependent:
        if major == 2 and minor >= 6:
            # must be >= 2.6 for log_lib
            python_version_major = 2
        elif major == 3 and minor >= 6:
            python_version_major = 3
        else:
            critical_str = 'Python version %d.%d.%d not supported' % \
                (major, minor, micro)
            sys.exit(critical_str)
            
        # temp:
        print('Supported Python version %d.%d.%d in log_lib' % \
                (major, minor, micro))
                
        # save the version awareness to the log object:
        self.major = major
        self.minor = minor
        self.micro = micro
            
        # the returnded python major version probably will not be used
        return python_version_major
        
    def define_log_path(self, path):
        self.log_path = path

    def define_debug_path(self, path):
        self.debug_path = path
        
    def define_log_level(self, level):
        self.level = level

    def define_screen_level(self, level):
        self.screen_level = level
        
    def log_file_remove(self):
        # remove the existing log file:
        if os.path.exists(self.log_path):
            try:
                os.remove(self.log_path)
            except:
                print('cannot remove file: %s' % self.log_path)
        
    def log_file_open(self):
        # potentially removing the existing file is left to the user
        # open for appending:
        fh = io.open(self.log_path, 'a', encoding=self.encoding)
        # self log file handle:
        self.fh = fh

    def log_file_flush(self):
        '''
        Make sure everything is written to the log file
        '''
        self.fh.flush()

    def debug_file_remove(self):
        # remove the existing file to start over:
        if os.path.exists(self.debug_path):
            try:
                os.remove(self.debug_path)
            except:
                print('cannot remove file: %s' % self.debug_path)

    def debug_file_open(self):
        # potentially removing the existing file is left to the user
        # open for appending:
        dh = io.open(self.debug_path, 'a', encoding=self.encoding)
        # self debug file handle:
        self.dh = dh

    def debug_file_flush(self):
        '''
        Make sure everything is written to the debug file
        '''
        self.dh.flush()
        
    def text_type(self, s):
        '''
        Convert s to a unicode text type of the current Python version.
        
        (for Python 2: unicode; for Python 3: str)
        '''
        res = str(s) if self.major == 3 else unicode(s)
        return res

    def gen_write(self, file_handler, s):
        file_handler.write(self.text_type(s))
        
    def log_file_append(self, s):
        self.gen_write(self.fh, s)

    def debug_file_append(self, s):
        self.gen_write(self.dh, s)

    def debug_separator(self, element='=', length=146):
        self.debug_file_append(element * length + '\n')
        
    # --------------------------------------------------------------------------
    
    def now_string(self):
        '''
        Return a string representing a current date and time stamp.
        
        ...or space equivalent, if time did not change too much.
        '''
        now = datetime.datetime.now()
        # ~ date_stamp_format = '%d.%m.%Y %H:%M:%S.%f'
        # no fractions of a second, as decided 30.03.2020 13:49:10:
        date_stamp_format = '%d.%m.%Y %H:%M:%S'
        now_str = now.strftime(date_stamp_format)
        if now_str == self.last_datetime_string:
            # the result will be a series of spaces:
            res = ' ' * (len(now_str))
        else:
            # now string has changed:
            res = now_str
            self.last_datetime_string = now_str
            
        return res

    
    # --------------------------------------------------------------------------
    log_levels = [
        'debug',
        'info',
        'warning',
        'error',
        'critical',
    ]
    
    
    # --------------------------------------------------------------------------
    # short identifiers of log levels:
    _level_id = {
        'debug': 'D',
        'info': 'I',
        'warning': 'W',
        'error': 'E',
        'critical': 'C',
    }
    # --------------------------------------------------------------------------
    # general log file writing function/method:
    
    def general_log_write(self, level, *sl, **kw):
        
        max_width = 120
        
        
        
        real_str_list = [str(s) for s in sl]
        message = ' '.join(real_str_list)
        
        if 'indent' in kw:
            indent = kw['indent']
        else:
            indent = 0
        
        # one or more strings could have been multiline;
        # split them to single line strings
        
        message_list = message.splitlines()
        
        # the prefix, including datetime stamp, will be common:
        
        pre_prefix = ''
        pre_prefix += self.now_string() + ' | '
        pre_prefix += self._level_id[level]

        if len(message_list) == 1:
            # the first or only line:
            prefix = pre_prefix + ' | '
        else:
            # continuation after the first line
            # different character plus 4 spaces indent:
            prefix = pre_prefix + ' | ' + 4 * ' '
        
        for i, one_message in enumerate(message_list):
            # logging and printing a single, possibly long line:
            
            # break the message to shorter lines, if possible:
            
            
            # ~ textwrap.wrap(text, width=max_width, **kwargs)
            mes_list = textwrap.wrap(one_message, width=max_width)
            
            for mes in mes_list:
                
                # all messages goes to the debugging log:
                self.debug_file_append(prefix + mes + '\n')

                # selected, level-dependent messages go to the main log:
                if level != 'debug':
                    if self.log_levels.index(level) >= self.log_levels.index(self.level):
                        # yes, log at the moment:
                        self.log_file_append(prefix + mes + '\n')

                # selected, level-dependent messages go to the screen:
                if self.log_levels.index(level) >= self.log_levels.index(self.screen_level):
                    
                    # possibly printing to a screen:
                    # without datetime stamps
                    print(mes)
    
    
    # --------------------------------------------------------------------------
        
    def debug(self, *sl, **kw):
        '''
        log and/or write to the console a debugging message
        '''
        self.general_log_write('debug', *sl, **kw)

    def info(self, *sl, **kw):
        '''
        log and/or write to the console an info level message
        '''
        self.general_log_write('info', *sl, **kw)

    def warning(self, *sl, **kw):
        '''
        log and/or write to the console a warning message
        '''
        self.general_log_write('warning', *sl, **kw)

    def error(self, *sl, **kw):
        '''
        log and/or write to the console an error message
        '''
        self.general_log_write('error', *sl, **kw)

    def critical(self, *sl, **kw):
        '''
        log and/or write to the console a critical information
        and stop the program
        '''
        self.general_log_write('critical', *sl, **kw)
        # make sure the files are flushed:
        self.debug_file_flush()
        self.log_file_flush()
        # and bye, bye:
        sys.exit()

        
        
        
# ------------------------------------------------------------------------------

def start_log(log_name=None, debug_name=None, log_level='debug',
        screen_level='info', remove=False):
    global log
    
    global debug
    global info
    global warning
    global error
    global critical

    global log_append
    global debug_append
    global debug_separator

    if log_name is None:
        log_name = 'algotype.log'
    if debug_name is None:
        debug_name = 'algotype_debug.log'
        
    log = Log_machinery(log_name, debug_name, remove=remove)
    log.define_log_level(log_level)
    log.define_screen_level(screen_level)

    debug = log.debug
    info = log.info
    warning = log.warning
    error = log.error
    critical = log.critical
    
    log_append = log.log_file_append
    debug_append = log.debug_file_append
    debug_separator = log.debug_separator
    
    # return the log object
    return log

