#!/usr/bin/python3
# -*- coding: utf-8 -*-

##!/usr/bin/env python

# author: Marek Ryćko
__author__ = 'Marek Ryćko <marek@do.com.pl>'

'''
at_lib
Algotype library
a library of functions for the Algotype system

19.02.2019 16:00:44
moved from 0.py and named as mp1_lib
as a library of functions
for a metatype1 system (mt1 in short)

7.3.2019 renamed to mt_lib

28.06.2019 00:33:13
renamed to at_lib (for: algotype library)
to be further removed
'''

# standard library
import re
#~ import itertools
#~ import copy # for copying/comparing dictionaries
#~ import json
import os
import shutil
# ~ import subprocess   
# json module for serialization of structures
import json

# Algotype:
from . import log_lib

# ------------------------------------------------------------------------------
# moving to directories:
# ------------------------------------------------------------------------------
def move_files(fdir, tdir, pattern):
    '''
    move all files in the fdir
    to the tdir
    if their names match the pattern
    '''
    source = fdir
    dest = tdir

    fl = os.listdir(source)
    
    rec = re.compile(pattern)

    for f in fl:
        mo = rec.match(f)
        if mo:
            # ~ log_lib.debug('moving', f, 'to', dest)
            shutil.move(f, dest)

def move_file(f, dest):
    '''
    move the file f
    to the dest
    if the file exists
    '''
    try:
        # ~ log_lib.debug('moving', f, 'to', dest)
        shutil.move(f, dest)
    # ~ except FileExistsError, FileNotFoundError:
    except:
        pass

def replace_file(f, d):
    '''
    move the file f
    to the destination d/f
    replacing if it exists
    '''
    try:
        f2 = os.path.join(d, f)
        os.replace(f, f2)
    except:
        pass



def make_directory(dirname):
    '''
    create a directory
    and possibly all the intermediate directories
    if they do not exist
    and do nothing if they exist
    '''
    try:
        # create the target directory:
        os.makedirs(dirname)
    # ~ except FileExistsError:
    except:
        pass

# ------------------------------------------------------------------------------
# renaming:
# ------------------------------------------------------------------------------

def rename_file(f1, f2):
    
    # ~ log_lib.debug('renaming', f1, 'to', f2) 
    try:
        os.rename(f1, f2)
    except:
        pass


def rename_eps(di, maxl=4):
    '''
    rename all the files
    in the directory di
    of the form
        filename.ext
    where the ext is 1 to 3 digits
    to names of the form
        filename.ext0
    where ext0 is 0001 or 0012 or 0123 (filled with 0s up to maxl length)
    
    '''
    max_ext_len = maxl

    # ~ pattern = r'.*\.([0-9]){1,' + str(max_ext_len) + r'3}'
    pattern = r'(.*)\.([0-9]+)'
    rec = re.compile(pattern)

    fl = os.listdir(di)
    for f in fl:
        # ~ log_lib.debug('moving', f, 'to', dest)
        mo = rec.match(f)
        if mo:
            # renaming is considered and subsequently performed
            # only for files matching the pattern
            fb = mo.group(1)
            ext = mo.group(2)
            if True:
            # ~ if len(ext) < max_ext_len:
                # file to be renamed
                # ~ new_ext = 'eps.' + ext.rjust(max_ext_len, '0')
                new_ext = ext.rjust(max_ext_len, '0') + '.eps'
                new_fn = fb + '.' + new_ext
                # ~ log_lib.debug('renaming', f, '-->', new_fn, 'from', ext, '-->', new_ext)
                # prepare full paths of files before and after renaming:
                path_source = os.path.join(di, f)
                path_dest = os.path.join(di, new_fn)
                # ~ log_lib.debug('renaming', path_source, '-->', path_dest)
                os.rename(path_source, path_dest)


# ------------------------------------------------------------------------------
# copying
# ------------------------------------------------------------------------------
def copy_file(f, dest):
    '''
    copy the file f
    to the dest (file or directory)
    if the file exists
    and generally if it is possible
    '''
    try:
        # ~ log_lib.debug('copying', f, 'to', dest)
        # copy2 copies also metadata and destination may be a directory
        shutil.copy2(f, dest)
    # ~ except FileExistsError, FileNotFoundError:
    # ~ except FileNotFoundError:
    except:
        log_lib.critical('error copying file', f, 'to', dest)


# ------------------------------------------------------------------------------
# removing files:
# ------------------------------------------------------------------------------

def file_remove(fn):
    try:
        os.remove(fn)
    except:
        pass

# ------------------------------------------------------------------------------
# opening files for reading and writing:
# ------------------------------------------------------------------------------
def open_r(fn):
    '''
    open a file for text reading in utf-8 encoding
    '''
    fh = open(fn, 'r', encoding='utf8')
    return fh




# ------------------------------------------------------------------------------
# write json representation:
# ------------------------------------------------------------------------------

def write_json(j, fn):
    '''
    write a Python structure j
    being a json structure
    (a mixture of dictionaries, lists, ints, booleans, strings, None’s)
    serialize it as a string
    and write to a file of a name fn
    '''
    s = json.dumps(j, indent=4, ensure_ascii=False)
    with open(fn, 'w') as fh:
        fh.write(s)

def read_json(fn):
    '''
    read and return a Python structure j
    being a json structure
    (a mixture of dictionaries, lists, ints, booleans, strings, None’s)
    deserializing it from a string
    read from a file of a name fn
    '''
    with open(fn, 'r') as fh:
        s = str(fh.read())
    j = json.loads(s)
    return j



# ------------------------------------------------------------------------------
# saving and restoring current directories (one level):
# ------------------------------------------------------------------------------

def mk_dir_save_change_restore():
    '''
    a closure for functions saving, changing and restoring
    current directories
    '''
    priv = {
        # ~ 'last_dir': None,
        'last_dir': [],
        # development info:
        # ~ 'dev': True,
        'dev': False,
        }

    def dir_save():
        # ~ priv['last_dir'] = os.getcwd()
        d = os.getcwd()
        priv['last_dir'].append(d)
        if priv['dev']:
            # ~ log_lib.debug('saving dir', priv['last_dir'])
            log_lib.debug('saving dir', d)

    def dir_change(d):
        if priv['dev']:
            log_lib.debug('changing dir', d)
        os.chdir(d)

    def dir_restore():
        d = priv['last_dir'].pop()
        if priv['dev']:
            log_lib.debug('restoring dir', d)
        os.chdir(d)

    res = {
        'dir_save': dir_save,
        'dir_change': dir_change,
        'dir_restore': dir_restore,
    }
    
    return res
    
dir_save_change_restore = mk_dir_save_change_restore()

dir_save = dir_save_change_restore['dir_save']
dir_change = dir_save_change_restore['dir_change']
dir_restore = dir_save_change_restore['dir_restore']




def compare_dictionaries(d1, d2):
    '''
    check if the dictionaries are the same
    '''
    shared_items = {k: d1[k] for k in d1 if k in d2 and d1[k] == d2[k]}
    
    # ~ log_lib.debug(len(d1), len(d2), 'shared items:', len(shared_items))
    
def deep_compare_dictionaries(d1, d2):
    '''
    compare dictionaries of dictionaries
    up to the second level
    '''
    shared_keys = set(d1.keys()).intersection(set(d2.keys()))
    # ~ print 'shared keys', shared_keys
    # ~ print 'all d1 keys', d1.keys()
    # ~ print 'all d2 keys', d2.keys()
    for k in shared_keys:
        compare_dictionaries(d1[k], d2[k])
