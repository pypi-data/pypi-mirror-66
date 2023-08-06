#!/usr/bin/python3
# -*- coding: utf-8 -*-

# make the file both Python 2 and Python 3 compatible
# probably not needed any more, as of 16.03.2020 20:07:02:
# ~ from __future__ import print_function

# author: Marek Ryćko
__author__ = 'Marek Ryćko <marek@do.com.pl>'

'''
config interpreter
the interpreter of a config language
and partially also
a general mechanism of a language

both Python2 and Python3 compatible

11.04.2019 20:25:18
start half a day ago from a simpler config interpreter
'''

# ------------------------------------------------------------------------------
'''
the language description (to be corrected):

the interpreter is initialized with a constant “memory”
    which is a Python dictionary with expressions/programs as values

the result of the execution of a dictionary
    is a dictionary with the results of executing values/programs
    
the result of executing a basic type: int, Boolean, string, None
    is the value itself
    
the result of executing a list of a form [f, x1, x2, ...]
    where the number of x1, x2, ... elements is zero or more
    is the result of running a built-in function f
    applied to the list [x1, x2, ...] as a parameter

the list of build-in functions is a part of the interpreter definition
    
notes to the language design:
infinite loops are to be avoided by user
'''
# ------------------------------------------------------------------------------
# for calculatig paths:
import os
# for the date-time language module
import datetime
# for paths cleaning:
import re

# Algotype:
import algotype.log_lib as log_lib

# ------------------------------------------------------------------------------
# so far outside of the language and the interpreter:
# ------------------------------------------------------------------------------

def translate_dict(d):
    '''
    translate a dictionary d to a dictionary e
    treating values of d’s items
    as “programs” to be run
    
    for each item k: d[k]
    execute d[k] as a program in the small language defined here
    in the interenal (constant) environment of the interpreter
    and passing the result of the execution
    to the resulting dictionary e, as e[k]
    
    '''
    exe = make_interpreter(d)
        
    return exe(d)






# ------------------------------------------------------------------------------
# iterpreter modules/brics:
# ------------------------------------------------------------------------------


def make_module_memory():
    '''
    a closure being an interpreter
    operating on a hidden resource (a memory: a dictionary)
    using carefully selected set of operations
    '''
    # the initial internal state:
    priv = {
        # the internal environment:
        'env': {},
    }
    
    def init(d):
        '''
        initialization of the internal state, of the interpreter module:
        '''
        # we do not bother to make a copy:
        priv['env'] = d
        return d
        
    # all the operations below take a string list sl, list of arguments
    # and return some value
    
    def use(sl):
        log_lib.debug(f"config interpreter; the function use: argument is {str(sl)}")
        return priv['env'][sl[0]]
       
    res = {
        'init': init,
        'use': use,
    }
        
    return res

def make_module_string():
    '''
    a closure being an interpreter
    specialized in operations on strings
    including operating system dependent operatiosn
    '''
        
    # all the operations below take a string list sl, list of arguments
    # and return some value
    
    def join(sl):
        '''
        join a string list sl
        using os.path.join
        '''
        simple = False
        sep = os.sep
        # ~ sep = r'\\'
        # ~ sep = r'|'
        if simple:
            res = os.path.join(*sl)
        else:
            path = os.path.normpath(os.path.join(*sl))
            # ~ log_lib.debug('before replacement %s' % path)
            # the following replacement does not work under Windows:
            # ~ res = re.sub(r'(\\\\|\/)', sep, path)
            # 31.12.2019 16:13:43:
            res = path
            # ~ log_lib.debug('not replacing %s --> %s' % (path, res))
        return res
        
    def ext(sl):
        '''
        take a list of strings at least two-element long
        join all but the last one using os.path.join
        and then join the last one as the filename extension
        '''
        fl = sl[:-1]
        f = os.path.join(*fl)
        r = f + os.extsep + sl[-1]
        return r

    def li(sl):
        '''
        return a string list sl
        '''
        return sl

        
    res = {
        'ext': ext,
        'join': join,
        'list': li,
    }

    return res

def make_module_date_time():
    '''
    a closure being an interpreter
    specialized in operations on date and time
    strings and values
    '''
        
    # all the operations below take a string list sl, list of arguments
    # and return some value
    
    def now_string(sl):
        '''
        join a string list sl
        using os.path.join
        '''
        s = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        log_lib.debug(f"date string: {s}")
        return s
        
    res = {
        'now': now_string,
    }

    return res


# ------------------------------------------------------------------------------

def make_modules():
    '''
    make a dictionary of the interpreter modules
    (here it is not configurable; just a program for this purpose)
    '''
    
    modules = {}
    
    modules['memory'] = make_module_memory()
    modules['string'] = make_module_string()
    modules['date_time'] = make_module_date_time()

    return modules


def make_interpreter(d):
    '''
    make an instance of the interpreter of this lanuage
    '''
    # create a local dictionary of modules:
    modules = make_modules()
    
    # initialize one of them (the one that needs it)
    modules['memory']['init'](d)
    
    def apply(f, x):
        '''
        take a function name (string) f
        and a structural parameter x
        and execute it
        by sending to an interpreter module
        via dns (translation of f to a (module name, function name) pair)
        
        this function (apply) is syntax independent
        also in the sense of a data-structure syntax
        it assumes the parsing (in any sense) has already been done
        '''

        log_lib.debug('config interpreter:', 'applying', f, 'of', str(x))
        module, function = dns(f)
        log_lib.debug('config interpreter:', 'module', module, 'function', function)
        res = modules[module][function](x)
        return res

    def exe(v):
        '''
        execute a “program” v,
        that is a single language expression in the language syntax
        of a form:
            -- either a basic value, like string, int, Boolean, None
            -- or a list [f, x1, x2, ...] denoting f(x1, x2, ...)
            -- or a dictionary {k1: v1, k2: v2... }, where all vi-s are to
               be executed
        '''
        strv = str(v)
        log_lib.debug(f"config interpreter; executing “program”: {strv}")
        if is_basic(v):
            # this is a final value; nothing to do
            res = v
        elif isinstance(v, list):
            # this should be a list with a string as a first parameter
            # later we could also calculate the function name
            # ~ log_lib.debug(v)
            # 1. parsing:
            f = v[0]
            # the list of parameters is everything, except the first (zero’s) one
            x = v[1:]
            # 2. calculate the parameters until the basic value is found:
            # execute (fully) each element of x
            # creating y:
            y = [exe_full(el) for el in x]
            # ~ log_lib.debug('config interpreter:', 'for', strv, 'f=%s' % f, 'x=%s' % str(x), 'y=%s' % str(y))
            log_lib.debug(f"config interpreter: for {strv} f={f}, {str(x)}, y={str(y)}")
            # 3. now apply the function f to the calculated parameteres y:
            res = apply(f, y)
            # ~ res = y
        elif isinstance(v, dict):
            # prepare a dictionary to collect new, translated items:
            # the values/programs v[k] are executed in an arbitrary order:
            res = {k: exe_full(v[k]) for k in v}
            # ~ if is_call(res):
                # ~ res = apply(res['f'], res['x'])
        log_lib.debug(f"config interpreter; result of executing {strv}: {str(res)}")

        return res

    def exe_full(v):
        ready = False
        command = v
        while not ready:
            command = exe(command)
            if is_basic(command):
                ready = True
        return command

    return exe
    
def is_call(v):
    return isinstance(v, dict) and 'f' in v and 'x' in v

def dns(f):
    '''
    take a string f, a function name
    and return a pair:
        a string name of an interpreter module
        a string name of a function within the module
    '''
    tr = {
        'l': ['string', 'list'],
        'list': ['string', 'list'],
        'j': ['string', 'join'],
        'join': ['string', 'join'],
        'ext': ['string', 'ext'],
        'x': ['string', 'ext'],
        'u': ['memory', 'use'],
        'use': ['memory', 'use'],
        'now': ['date_time', 'now'],
    }
    return tr[f]


def is_basic(v):
    '''
    check if v is one of basic datatypes
    (no unicode allowed in Python 2 config)
    '''
    return isinstance(v, (bool, int, str)) or v is None

# ------------------------------------------------------------------------------

