#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
python3 program
generating and installing ff_make_font (Python 2 or 3) directory and modules
21.03.2020 17:19:06

This file is generated automatically from a template and
copies of several files transfomed to strings;
please -- do not edit the generatedy .py file
(only the template file .template.py and the component
files are to be edited)
'''

import os
import sys
import shutil

# Algotype:
import algotype.log_lib as log_lib

# ------------------------------------------------------------------------------
# strings containing copies of files:
# ------------------------------------------------------------------------------

# files of ff_make_font package:

init_str = r""""""
at_lib_str = r"""#!/usr/bin/python3
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
"""
ff_make_font_str2 = r"""#!/usr/bin/python
# -*- coding: utf-8 -*-

# make parts of the file both Python 2 and Python 3 compatible
from __future__ import print_function
'''
ff_make_font
FontForge make font
17.03.2020 17:16:56

previously (in Metatype1) known as FFDKM:
(FFDKM was "Python FontForge based Developement Kit for Metatype1")

A converter of METAPOST glyphs into Type1 and OpenType (CFF).
Includes advanced OpenType features and math functionality.

'''

__author__ = u"Piotr Strzelczyk, Marek Ryćko and Bogusław Jackowski"
__copyright__ = "Copyright (c) 2017, 2020 by GUST e-foundry"
__credits__ = ["Piotr Strzelczyk", u'Marek Ryćko', u"Bogusław Jackowski", "Piotr Pianowski"]
__license__ = "GPL"
__maintainer__ = u'Marek Ryćko'
__email__ = "marek@do.com.pl"
__status__ = "Beta"

# python standard library:
import os.path
import sys
import string
import re
import gc
from argparse import ArgumentParser
# json module for serialization of structures
import json

# Algotype library:
from . import at_lib as lib
from . import log_lib

# ReportLab PFM library; part of the ReportLab PDF Toolkit:
# (possibly in the form adaptede to Python3 by Marek Ryćko
from .pfm import PFM

# FontForge python bindings:
# logging, using log_lib, is not yet possible;
# we are before reading arguments
try:
    import fontforge
except ImportError:
    # ~ log_lib.critical(u'FontForge must be compiled with --pyextension.')
    sys.exit(u'FontForge must be compiled with --pyextension.')
if not hasattr(fontforge, 'math'):
    # ~ log_lib.critical(u'Too old FontForge — doesn’t support MATH table.')
    sys.exit(u'Too old FontForge — doesn’t support MATH table.')

# ------------------------------------------------------------------------------
# to further library:
# ------------------------------------------------------------------------------
def write_file(s, fn, mess):
    '''
    create a file of a filename fn
    write a string s to this file in a text mode
    and display a critical error message in case of error
    '''
    try:
        # create a file handler:
        fh = open(fn, 'w')
    except IOError:
        log_lib.critical(mess + ': %s' % fn)

    fh.write(s)
    fh.close()

# ------------------------------------------------------------------------------
# reading data from a json font file
# and storing it in a font generated by some engine
# (fontforge as of 01.04.2019 13:03:19)
# ------------------------------------------------------------------------------




# ------------------------------------------------------------------------------
# setting metainformation (global parameters) of the font:
# ------------------------------------------------------------------------------

    
    
def json_font_parameters_to_font(par):
    '''
    read a dictionary (a json structure) of font parameters
    and put it into a fontforge font structure
    font is a global variable (so far)
    '''

    def set_names(names):
        # ~ log_lib.debug('names', names)
        for l, d in names.items():
            for i in d:
                # ~ font.appendSFNTName(l, i, d[i])
                # 19.08.2019 19:45:22:
                # after serialization and deserialization to and from json
                # the l and i values were unicode instead of string
                # ~ if str(l).lower() in ('ascender', 'capheight'):
                # ~ log_lib.debug('Setting SFNT table in FontForge font', str(l), str(i), d[i])
                font.appendSFNTName(str(l), str(i), d[i])

    def set_attributes(attr):
        for a, v in attr.items():
            try:
                log_lib.debug('Setting font attribute in FontForge font %s: %s' \
                    % (str(a), str(v)))
                setattr(font, a, v)
            except:
                # the nonexistent attributes are almost silently skipped:
                message = 'It’s OK, that we do not set the (nonexisting) font attribute: %s' % a
                log_lib.debug(message)

    # --------------------------------------------------------------------------
    # writing:

    # constant for Algotype:
    font.em = par['em']

    # write information from names and attr dictionaries
    # to the FontForge font object:
    # ~ log_lib.debug(par['names'])
    set_names(par['names'])
    set_attributes(par['attr'])
    
    # "ASCENDER": "694.44444"
    # ~ log_lib.debug('font.ascent', font.ascent)
    # ~ font.ascent = 695.55555
    # ~ log_lib.debug('changed font.ascent to', font.ascent)

    font.sfntRevision = par['revision']
    
    if par['pan'] is not None:
        font.os2_panose = tuple(par['pan'])

    # write oti font bold and italic attributes to the FontForge font structure:

    # ~ log_lib.debug('stylemap', font.os2_stylemap)
    # result: 0
    # ~ log_lib.debug('weight', font.os2_weight)
    # result: 400
    
    ff_bold = 32
    ff_bold_weight = 700
    ff_italic = 1
    ff_regular = 64
    
    if par['bold']:
        font.os2_weight = ff_bold_weight
        font.os2_stylemap |= ff_bold

    if par['italic']:
        font.os2_stylemap |= ff_italic
        
    # PSt: why < 1 ?
    if font.os2_stylemap < 1:
        font.os2_stylemap = ff_regular    
    
# ------------------------------------------------------------------------------
# glyphs to encoding:
# ------------------------------------------------------------------------------


def encoding_structure_to_string(encd):
    '''
    MR, 24.02.2019 13:48:49
    partially based on PSt’s function set_encoding.
    take an encoding structure, based on oti_gly structure
    and serialize it as a string
    to be further written to a file
    and input to fontforge
    '''
    enc = encd['enc']
    encname = encd['encname']

    # string list sl (line list):
    sl = []

    # generate the lines:
    sl.append('/%s[' % encname)
    for i in range(256):
        sl.append('/%s' % enc[i])
    sl.append('] def')
    
    # join lines making the string:
    s = '\n'.join(sl)
    # ~ log_lib.debug(s)
    return s

def set_encoding(es):
    '''
    this set_encoding function
    and the encoding name encname
    from the encoding structure es
    prepared from oti_gly (part of structure read from oti file)
    
    it is a refactored version of set_encoding by Piotr Strzelczyk, PSt
    refactoring by MR
    on 24.02.2019 14:27:09
    '''
    
    s = encoding_structure_to_string(es)

    # ~ fn = iname + '_PFB.enc'
    # 24.06.2019 23:33:29:
    fn = iname + '_pfb.enc'
    mess = "Couldn't create ENC file"
    # temp file for fontforge:
    write_file(s, fn, mess)
        
    fontforge.loadEncodingFile(fn)
    encname = es['encname']
    font.encoding = encname
    # cleaning up:
    # ~ os.remove(fn)


# ------------------------------------------------------------------------------
# including adobe feature files (as strings) to the font:
# ------------------------------------------------------------------------------

def feature_strings_to_font(features):
    '''
    read features, a list of strings
    each representing an adobe feature file
    and put them to the fontforge font
    
    '''
    # ~ log_lib.debug('features as a list:', features)
    for fs in features:
        # fs is a feature string
        # write it to a temporary file
        # and put into the font
        # write feature string to a temporary file:
        
        # temp_dir is already created, by oti_to_font
        fea_path = os.path.join(temp_dir, 'feature.fea')
        try:
            fh = open(fea_path, 'w')
            fh.write(fs)
            fh.close()
            font.mergeFeature(fea_path)
        except EnvironmentError, IOError:
            log_lib.error("Couldn't find FEA file: %s" % fnm)

# ------------------------------------------------------------------------------


def fix_afm(afmname, oti):
    try:
        frafm = open(afmname, 'r')
    except IOError:
        log_lib.critical("Couldn't read (created) AFM file: %s" % afmname)
    AFMT = []
    for line in frafm.readlines():
        AFMT.append(line.rstrip())
    frafm.close()
    for i in range(len(AFMT)):
        if 'StartCharMetrics' in AFMT[i]:
            com_ins=i
        if '; L' in AFMT[i]:
            AFMT[i]=remove_ligatures_dup(AFMT[i])
    AFMT[com_ins:com_ins] = afm_tfm_comments(oti)
    try:
        fwafm = open(afmname, 'w')
    except IOError:
        log_lib.critical("Couldn't write AFM file: %s" % afmname)
    for l in AFMT:
      fwafm.write(l + '\n')
    fwafm.close()

def afm_tfm_comments(oti):
    '''
    a maintained copy of this function is now in afm_lib
    this functions’s existence here will become obsolete
    '''
    res = []
    if 'PFM_NAME' in oti:
        res.append('Comment PFM parameters: %s %s %s %s' % (oti['PFM_NAME'], 
          oti['PFM_BOLD'], oti['PFM_ITALIC'], oti['PFM_CHARSET']))
    if 'DESIGN_SIZE' in oti:
        res.append('Comment TFM designsize: %s (in points)' % (oti['DESIGN_SIZE']))
    if 'FONT_DIMEN' in oti:
        fd=oti['FONT_DIMEN']
        fn=oti['DIMEN_NAME']
        for i in range(256):
            s=str(i)
            if s in fd:
                res.append('Comment TFM fontdimen %2s: %-10s %s' % (s, fd[s], fn[s]))
    if 'HEADER_BYTE' in oti:
        hb=oti['HEADER_BYTE']
        for i in ('9', '49', '72'):
            if i in hb:
                res.append('Comment TFM headerbyte %2s: %s' % (i, hb[i]))
    return res

def fix_pfm(pfmname, oti):
    try:
        pfm = PFM(pfmname)
    except IOError:
        log_lib.critical("Couldn't read (created) PFM file: %s" % pfmname)
        return
    if 'PFM_CHARSET' in oti:
        pfm.dfCharSet = int(oti['PFM_CHARSET'], 16)
    if 'PFM_ITALIC' in oti:
        # ~ log_lib.debug("oti['PFM_ITALIC']", oti['PFM_ITALIC'])
        if pfm.dfItalic != int(oti['PFM_ITALIC']):
           log_lib.warning("Bad Italic bit in result PFM file: %s" % pfmname)
    if 'PFM_BOLD' in oti:
        if (pfm.dfWeight > 500) != int(oti['PFM_BOLD']):
          log_lib.warning("Bad Weight info in result PFM file: %s" % pfmname)
    pfm.write_to_file(pfmname)
    
def remove_ligatures_dup(afl):
    src=afl.split(';')
    res=[]
    ligs={}
    for f in src:
        if f not in ligs:
            res.append(f)
            ligs[f]=1
    return ';'.join(res)

# ------------------------------------------------------------------------------
# glyph outlines:
# ------------------------------------------------------------------------------

def kern_info_to_font(kerns):
    '''
    take a json kerns structure
    and put the kerns into the fontforge font structure
    font and gly_dic are global substructures within fontforge
    '''

    font.addLookup('kerns', 'gpos_pair', (), (("kern", (("DFLT", ("dflt",)),("latn", ("dflt",)))),) )
    font.addLookupSubtable('kerns', 'kerns0')

    for gly, inf in kerns.items():
        # ~ log_lib.debug(gly, inf)
        # inf is a dictionary of kerns (from glyph names to int kern values)
        glyph = gly_dic[gly]
        for g, val in inf.items():
            # ~ glyph.addPosSub('kerns0', g, val)
            # 12.10.2019 20:09:25:
            # val can be any number, especially int or float:
            glyph.addPosSub('kerns0', g, int(round(val)))


# ------------------------------------------------------------------------------
# glyph outlines:
# ------------------------------------------------------------------------------


def json_to_glyphs(gj):
    '''
    write a json glyph structure (a dictionary of single json glyphs)
    to a fontforge font structure
    '''
    
    # ~ paths_source = 'eps'
    paths_source = 'json'
    
    for gly, g in gj.items():
        # gly is a glyph identifier
        # g is a single glyph json structure
        # ~ log_lib.debug('generating [' + gly + ', ' + str(g['codepoint']) + ']')
        codepoint = -1 if g['codepoint'] is None else g['codepoint']
        # ~ log_lib.debug('generating [' + gly + ', ' + str(codepoint) + ']')
        # ~ log_lib.debug(str(g['eps']))
        
        # codepoint may be -1, -10 or a positive value
        if codepoint != -10:
            # the glyph not to be skipped
            
            glyph = font.createChar(codepoint, gly)

            if 0:
                # old code:

                # write eps info to the fontforge glyph:
                if g['eps'] is not None:
                    # too small eps strings are equivalent to empty:
                    if len(g['eps']) > 180:
                        if paths_source == 'eps':
                            # 1.
                            # write eps to a temporary file:
                            eps_path = os.path.join(temp_dir, 'glyph.eps')
                            fh = open(eps_path, 'w')
                            fh.write(g['eps'])
                            fh.close()
                            # 2. write the paths in eps to the glyph:
                            try:
                                glyph.importOutlines(eps_path)
                            except:
                                log_lib.error("Cannot import outline for glyph:\n  %s" % gly)
                        elif paths_source == 'json':
                            # create a fontforge glyph path info
                            # in the glyph element of a fontforge font
                            # from a structural information from a json structure:
                            json_to_glyph(g, glyph)
                        else:
                            # no other sources are implemented now:
                            pass
                        glyph.correctDirection()
                        glyph.canonicalStart()
                        glyph.canonicalContours()
                    else:
                        glyph.changed=True
                        pass
                else:
                    # ~ log_lib.warning("Missing EPS info in OTI for glyph:\n  %s" % gly)
                    pass

            else:
                # new code, as of 10.12.2019 21:46:56:
                
                
                # write eps info to the fontforge glyph:
                if 'paths' in g:
                    # empty paths are not written:
                    if len(g['paths']['us']) > 0:
                        if paths_source == 'eps':
                            # 1.
                            # write eps to a temporary file:
                            eps_path = os.path.join(temp_dir, 'glyph.eps')
                            fh = open(eps_path, 'w')
                            fh.write(g['eps'])
                            fh.close()
                            # 2. write the paths in eps to the glyph:
                            try:
                                glyph.importOutlines(eps_path)
                            except:
                                log_lib.warning("Cannot import outline for glyph:\n  %s" % gly)
                        elif paths_source == 'json':
                            # create a fontforge glyph path info
                            # in the glyph element of a fontforge font
                            # from a structural information from a json structure:
                            json_to_glyph(g, glyph)
                        else:
                            # no other sources are implemented now:
                            pass
                        glyph.correctDirection()
                        glyph.canonicalStart()
                        glyph.canonicalContours()
                    else:
                        glyph.changed=True
                        pass
                else:
                    # ~ log_lib.warning("Missing EPS info in OTI for glyph:\n  %s" % gly)
                    pass

            # write metrical info to the fontforge glyph:
            # moved after putting path info to the gliph on 25.09.2019 22:08:25:
            m = g['metrics']
            if 'width' in m:
                glyph.width = m['width']
                # experiment, 14.10.2019 14:54:25:
                # ~ glyph.width = 888.777
            if 'textheight' in m:
                glyph.texheight = m['textheight']
            if 'textdepth' in m:
                glyph.texdepth = m['textdepth']


        else:
            pass
            log_lib.debug('not generating (skipping) [' + gly + ', ' + str(codepoint) + ']')



def json_to_glyph(g, glyph):
    '''
    create a fontforge glyph path info
    in the glyph element of a fontforge font
    from a structural information from a json structure
    '''
    pen = glyph.glyphPen()

    # ~ grammar_data = [
        # ~ ['setrgbcolor', 3],
        # ~ ['newpath', 0],
        # ~ ['moveto', 2],
        # ~ ['lineto', 2],
        # ~ ['curveto', 6],
        # ~ ['lineto', 2],
        # ~ ['closepath', 0],
        # ~ ['fill', 0],
        # ~ ['showpage', 0],
    # ~ ]
    
    commands = g['paths']['us']
    
    for com in commands:
        # execute a fontforge counterpart of a command
        f = com['t']
        x = com['v']
        if f in ('setrgbcolor', 'setgray', 'fill', 'showpage'):
            pass
        if f in ('newpath',):
            pass
        elif f == 'moveto':
            pen.moveTo((x[0], x[1]))
        elif f == 'lineto':
            pen.lineTo((x[0], x[1]))
        elif f == 'curveto':
            pen.curveTo((x[0], x[1]), (x[2], x[3]), (x[4], x[5]), )
        elif f == 'closepath':
            pen.closePath()
        else:
            pass

# ------------------------------------------------------------------------------



def prepare_OS2(attr, n, v):
#      os2_version = 5
#    + FSType <number>;            os2_fstype
#    + Panose <panose number>;     os2_panose
#    - UnicodeRange <Unicode range list>;  os2_unicoderanges
#    - CodePageRange <code page list>;  os2_codepages
#    + TypoAscender <metric>;      os2_typoascent, os2_typoascent_add
#    + TypoDescender <metric>;     os2_typodescent, os2_typodescent_add
#    + TypoLineGap <metric>;       os2_typolinegap
#    + winAscent <metric>;         os2_winascent, os2_winascent_add
#    + winDescent <metric>;        os2_windescent, os2_windescent_add
#    - XHeight <metric>;           -- readonly in FF
#    - CapHeight <metric>;         -- readonly in FF
#    + WeightClass <number>;       +- os2_weight
#    + WidthClass <number>;        +- os2_width
#    + Vendor <string>;            os2_vendor
#    ? LowerOpSize <number>;
#    ? UpperOpSize <number>;
#   -- AvgCharWidth     
#      SubscriptXSize              os2_subxsize
#      SubscriptYSize          os2_subysize
#      SubscriptXOffset        os2_subxoff
#      SubscriptYOffset        os2_subyoff
#      SuperscriptXSize        os2_supxsize
#      SuperscriptYSize        os2_supysize
#      SuperscriptXOffset      os2_supxoff
#      SuperscriptYOffset      os2_supyoff
#      StrikeoutSize               os2_strikeysize
#      StrikeoutPosition       os2_strikeypos
#   -- sFamilyClass                os2_family_class
#      fsSelection  
#          0    bit 1   ITALIC     Font contains italic or oblique characters.
#          1        UNDERSCORE Characters are underscored.
#          2        NEGATIVE   Characters have their foreground and background reversed.
#          3        OUTLINED   Outline (hollow) characters, otherwise they are solid.
#          4        STRIKEOUT  Characters are overstruck.
#          5    bit 0   BOLD       Characters are emboldened.
#          6        REGULAR    Characters are in the standard weight/style for the font.
#          7 os2_use_typo_metrics        USE_TYPO_METRICS If set, it is strongly recommended to use
#                                  OS/2.sTypoAscender - OS/2.sTypoDescender+ OS/2.sTypoLineGap
#                                  as a value for default line spacing for this font.
#          8 os2_weight_width_slope_only WWS The font has ‘name’ table strings consistent with
#                                  a weight/width/slope family without requiring use of ‘name’
#                                  IDs 21 and 22.
#   -- DefaultChar  
#      BreakChar    
#      MaxContext
    OS2fields = {
       'SubscriptXSize'   : 'os2_subxsize',
       'SubscriptYSize'   : 'os2_subysize',
       'SubscriptXOffset' : 'os2_subxoff',
       'SubscriptYOffset' : 'os2_subyoff',
       'SuperscriptXSize' : 'os2_supxsize',
       'SuperscriptYSize' : 'os2_supysize',
       'SuperscriptXOffset': 'os2_supxoff',
       'SuperscriptYOffset': 'os2_supyoff',
       'StrikeoutSize'     : 'os2_strikeysize',
       'StrikeoutPosition' : 'os2_strikeypos',
    }
    if n in OS2fields:
        attr[OS2fields[n]] = int(v)


def set_variants(vari):
    for ch, t, hv, rest in vari:
        try:
            gl = gly_dic[ch]
        except KeyError:
            log_lib.warning("Glyphname %s (used in math parameters) absent from font" % ch)
            continue
        if t == 'var':
            ls = rest.split()
            lss = []
            if ls[0] != ch:
                lss.append(gl.glyphname)
            for c in ls:
                if c in gly_dic:
                    lss.append(gly_dic[c].glyphname)
                else:
                    log_lib.warning("Glyphname %s (used in math parameters) absent from font" % c)
            lss = ' '.join(lss) # must be glyphs NOT glyphs name!
            # log_lib.debug(lss)
            if hv == 'h':
                gl.horizontalVariants = lss
            else:
                gl.verticalVariants = lss
        elif t == 'ext':
            r = re.sub(' *}', '}', re.sub(' *{ *', '{', re.sub(' *, +', ',', rest)))
            ls = r.split()
            lss = []
            for c in ls:
                m = re.search(r'([A-Za-z0-9_\.]+){([0-1]),([0-9]+),([0-9]+),([0-9]+)}', c)
                if m:
                    cc = m.group(1)
                    if cc in gly_dic:
                        lss.append((gly_dic[cc], m.group(2) == '1',
                           int(m.group(3)), int(m.group(4)), int(m.group(5))))
                else:
                    log_lib.error("Invalid format of extension data: %s" % c)
            #log_lib.debug(lss)
            if hv == 'h':
                gl.horizontalComponents = lss
            else:
               gl.verticalComponents  = lss

def set_itcor(itcor):
    for ch, t, v in itcor:
        if ch in gly_dic:
            if t == 'ext':
                if font[ch].verticalComponents:
                     font[ch].verticalComponentItalicCorrection = int(v)
                elif font[ch].horizontalComponents:
                     font[ch].horizontalComponentItalicCorrection = int(v)
                else:
                    log_lib.warning("Extension italic correction set for glyph %s, without components" % ch)
            else:
                font[ch].italicCorrection = int(v)
        else:
            log_lib.warning("Glyphname %s (used in math accent_axes) absent from font" % ch)

def set_vertex(verx):
    for ch, t, w in verx:
        if ch in gly_dic:
            v = w.split()
            v.append('29999')
            l = len(v)
            if l < 4 or l % 2 > 0:
                log_lib.error("Missformed math kern line for glyph %s" % ch)
            tt = tuple([(int(v[2*i]), int(v[2*i+1])) for i in range(l/2)])
            # tt = tuple(zip(*[iter(v)]*2))
            p = -29999
            for v, h in tt:
                if h<p:
                    log_lib.error("Missformed math kern line for glyph %s" % ch)
                p = h
            if p != 29999:
                log_lib.error("Missformed math kern line for glyph %s" % ch)
            # log_lib.debug(tt)
            if t == 'ur':
                font[ch].mathKern.topRight = tt
            elif t == 'ul':
                font[ch].mathKern.topLeft = tt
            elif t == 'lr':
                font[ch].mathKern.bottomRight = tt
            elif t == 'll':
                font[ch].mathKern.bottomLeft = tt
            else:
                log_lib.warning("Unknown type of math kern: %4s in %s" % (t, ch))
        else:
            log_lib.warning("Glyphname %s (used in math kerning) absent from font" % ch)

def set_axis(axi):
    for ch, v in axi:
        if ch in gly_dic:
            font[ch].topaccent = int(v)
        else:
            log_lib.warning("Glyphname %s (used in math accent_axes) absent from font" % ch)

def set_extend(ext):
    for ch in ext:
        if ch in gly_dic:
            font[ch].isExtendedShape = True
        else:
            log_lib.warning("Glyphname %s (used in math is_extented) absent from font" % ch)

def set_extrapars(xpars):
    for xp in xpars:
        m = re.search(r'^(.+) *[=#] *(.+)$', xp)
        if m and m.group(1) == 'use_typo_metrics':
           if m.group(2) in ('0','1'):
               font.os2_use_typo_metrics = int(m.group(2))
           else:
               log_lib.error("Inproper value of use_typo_metrics: %s" % m.group(2))
        elif m and m.group(1) == 'set_ps_names':
           if m.group(2) == '1':
               copy_ttf_to_ps_names();
           elif m.group(2) != '0':
               log_lib.error("Inproper value of set_ps_names: %s" % m.group(2))
        elif m:
           log_lib.warning("Unrecognised extra parametr: %s" % m.group(1))
        else:
           log_lib.error("Invalid format of extra parametr: %s" % xp)


def copy_ttf_to_ps_names():
    for t in font.sfnt_names:
        if t[1]=='Copyright':
             font.copyright=t[2]
        if t[1]=='Family':
             font.familyname=t[2]
        if t[1]=='SubFamily':
             pass
        if t[1]=='Fullname':
             font.fullname=t[2]
        if t[1]=='PostScriptName':
             font.fontname=t[2] # always the same as Fullname?
    # font.version
    # font.sfntRevision = round(float(font.version)*65536)/65536

def calculate_private_dict():
    priv=font.private
    for ent in ['BlueValues', 'OtherBlues', 'StdHW', 'StdVW', 
      'StemSnapH', 'StemSnapV', 'BlueShift', 'BlueScale']:
        priv.guess(ent)
    if len(priv['BlueValues'])>1 and priv['BlueValues'][1]!=0: # first have to be baseline
        log_lib.debug("Correcting Blue values")
        bv=[v for v in priv['BlueValues']]
        bv[1]=0
        priv['BlueValues']=tuple(bv)
    # corect language tuple of 'kern' feature:
    kern_slt=None
    for ln in font.gsub_lookups:
        l_t, l_f, feat_slt = font.getLookupInfo(ln)
        if len(feat_slt) and feat_slt[0][0]=='salt':
            kern_slt=(('kern',feat_slt[0][1]),)
    if kern_slt:
        font.lookupSetFeatureList('kerns',kern_slt)
        
        
# ------------------------------------------------------------------------------
# renaming glyphs in the font
# according to goadb info:
# ------------------------------------------------------------------------------

def rename_glyphs(alias, unic=None):
    # if unic != None it is main name change and unicode numbering,
    # else it is only name for Type1 change
    #
    # below byway due to `glyphnameIsComponent()'
    # used by .glyphname to find associated names
    
    def sanit(n):
        return re.sub(r'\.','!!!',n)
    def tinas(n):
        return re.sub(r'!!!','.',n)

    if unic:
        log_lib.info('renaming glyphs')
        # no counting steps, as of 15.12.2019 22:44:44:
        # ~ log_lib.info("GLYPH rename: 1")
        # made even more quiet, 11.04.2019 00:06:40:
        # log_lib.debug("almost done")
    for g in gly_lst:
        if '.' in g.glyphname:
            g.glyphname = sanit(g.glyphname)

    if unic:
        # 15.12.2019 22:45:04:
        # ~ log_lib.debug("  2")
        pass
    for n, g in gly_dic.items():
        if unic:
            if n in alias:
                if n != alias[n]:
                    g.glyphname = sanit(alias[n])
                if n in unic:
                    ffunic = g.unicode
                    if  ffunic != unic[n] and unic[n] != -10:
                        if ffunic > 0 and unic[n] < 0:
                            log_lib.warning("%-20s %04x unicode not in GOADB" % (n, ffunic))
                        elif ffunic < 0 and unic[n] > 0:
                            pass # irrelevant info
                            # log_lib.warning("%-20s %04x unicode not in FF" % (n, unic[n]))
                        elif ffunic > 0 and unic[n] > 0:
                            log_lib.warning("%-20s %04x in GOADB, %04x in FF" % (n, unic[n], ffunic))
                        else:
                            log_lib.error("%-20s can't happen" % n)
                        g.unicode = unic[n]
            else:
                if g.unicode > 0:
                    log_lib.warning("%-20s %04x not in GOADB" % (n, g.unicode))
                else:
                    log_lib.warning("%-20s not in GOADB" % n)
        else:
            n = tinas(g.glyphname) # `current' glyphname
            if n in alias and n != alias[n]:
                g.glyphname = sanit(alias[n])
                    
    if unic:
        # 15.12.2019 22:45:18:
        # ~ log_lib.debug("  3")
        pass
    for g in gly_lst:
        if '!!!' in g.glyphname:
           g.glyphname = tinas(g.glyphname)

    if unic:
        # 15.12.2019 22:45:35:
        # ~ log_lib.debug("  4 -- done")
        pass

def remove_redundant_glyphs(goadb):
    for k, v in gly_dic.items():
        # ~ log_lib.debug('considering for removal (old name %s)' % k)
        if k in goadb['unic']:
            # ~ log_lib.debug('considering for removal (old name %s): %s' % (k, goadb['alias'][k]))
            if goadb['unic'][k] == -10:
                # ~ log_lib.debug('key:', k, 'unic of key:', goadb['unic'][k], 'alias of key:', goadb['alias'][k])
                if 0:
                    log_lib.debug('glyph to be removed (old name %s): %s' % (k, goadb['alias'][k]))
                # ~ font.removeGlyph(goadb['alias'][k])
                # 19.08.2019 19:47:47:
                # if goadb['alias'][k] was unicode, the fontforge asked for an integer:
                # the glyph to be skipped was not put to the font earlier, so there is
                # no need to remove it:
                try:
                    font.removeGlyph(str(goadb['alias'][k]))
                except:
                    log_lib.error('failed removing glyph %s from the font' % str(goadb['alias'][k]))
                
# ------------------------------------------------------------------------------


def validate_font():
    warn = []
    def addwarn(w, v, m, s):
        if v&m:
            if s:
                if len(w): w.append(', %s' % s)
                else: w.append('%s' % s)
            return v - m
        else:
            return v
    font.validate(1)
    for n, g in gly_dic.items():
        if g.validation_state > 1:
            v = g.validation_state
            w = []
            v=addwarn(w, v, 0x1, None)
            v=addwarn(w, v, 0x2, 'open contour')
            v=addwarn(w, v, 0x4, 'contours intersections')
            v=addwarn(w, v, 0x8, 'wrong direction of contour')
            v=addwarn(w, v, 0x200, 'invalid glyph name')
            v=addwarn(w, v, 0x100000, 'missing anchor')
            v=addwarn(w, v, 0x200000, 'duplicate glyph name')
            v=addwarn(w, v, 0x400000, 'duplicate unicode')
            v=addwarn(w, v, 0x20, None) # 'missing extrema in path'
            v=addwarn(w, v, 0x80, 'too many points in glyph')
            v=addwarn(w, v, 0x100, 'too many hints in glyph')
            v=addwarn(w, v, 0x40000, 'points toofar apart')
            if v > 0: w.append(', unrecognized warning: %x' % v)
            if len(w):
                 warn.append('%-20s' % (n + ':'))
                 warn.extend(w)
                 warn.append('\n')
    v = font.privateState    
    w = []
    v=addwarn(w, v, 0x1, 'odd number of elements in Blue')
    v=addwarn(w, v, 0x2, 'elements in Blue are disordered')
    v=addwarn(w, v, 0x4, 'too many elements in Blue')
    v=addwarn(w, v, 0x8, 'elements in Blue are too close')
    v=addwarn(w, v, 0x10000, 'missing BlueValues')
    v=addwarn(w, v, 0x20000, 'bad BlueFuzz')
    v=addwarn(w, v, 0x40000, 'bad BlueScale')
    if v > 0: w.append(', unrecognized warning: %x' % v)
    if len(w):
         warn.append('%-20s' % ('Private:'))
         warn.extend(w)
         warn.append('\n')
         
    # prepare the warning multiline string
    if len(warn) == 0:
        warn.append('No warnings found')
    warning_string = '\n'.join(warn)
    # write the multiline string:
    log_lib.warning(warning_string)
    # not writing the warnings to a special file, separate from logs
    # as of 20.04.2020 23:04:31
    

# ------------------------------------------------------------------------------
# Start of processing:
# ------------------------------------------------------------------------------



# ~ font = None
# ~ gly_dic = None
# ~ gly_lst = None


# ~ iname
# ~ bname
# ~ edir
# ~ ename
# ~ oname
# ~ jgname
# ~ joname
# ~ jfname
# ~ otiname
# ~ temp_dir
# ~ tname
# ~ sname
# ~ fename
# ~ gname
# ~ afname
# ~ mtname
# ~ extrapars
# ~ aalt
# ~ ahint
# ~ acorr
# ~ ovaname
# ~ ofename
# ~ quiet
# ~ pydir













def main():

    # awful global variables; the remainder after old Metatype1; sorry
    # to be cleaned up in the fututre, as of 18.03.2020 22:41:54

    global font
    global gly_dic
    global gly_lst
    
    
    global iname
    global bname
    global edir
    global ename
    global oname
    global jgname
    global joname
    global jfname
    global otiname
    global temp_dir
    global tname
    global sname
    global fename
    global gname
    global afname
    global mtname
    global extrapars
    global aalt
    global ahint
    global acorr
    global ovaname
    global ofename
    global quiet
    global pydir

    # ------------------------------------------------------------------------------
    
    

    # ------------------------------------------------------------------------------
    # reading arguments:
    # ------------------------------------------------------------------------------
    argpars = ArgumentParser(description='Algotype: Type1 or OpenType converter',
         fromfile_prefix_chars='@')
    addarg=argpars.add_argument
    addarg('input', help='Input Algotype filename')
    # 20.02.2019 00:41:15:
    addarg('-e', '--epsdir', nargs='?', const=False, help='Directory for input EPS files')
    addarg('-p', '--pydir', nargs='?', const=False, help='Directory for Python input files')
    addarg('-o', '--output', nargs='?', const=False, help='Generated OTF file')
    addarg('-te', '--tempdir', nargs='?', const=False, help='Temporary directory')
    addarg('-oti', '--oti', nargs='?', const=False, help='Oti file')
    addarg('-jg', '--jsongoadb', nargs='?', const=False, help='Json goadb file')
    addarg('-jo', '--jsonoti', nargs='?', const=False, help='Json oti file')
    addarg('-jf', '--jsonfont', nargs='?', const=False, help='Json font file')
    addarg('-t', '--typeone', nargs='?', const=False, help='Generated Type1 file')
    addarg('-s', '--save', nargs='?', const=True, help='Output saved in sfd format')
    addarg('-f', '--fea', nargs='*', help='Feature filename to be used')
    addarg('-g', '--goadb',  nargs='?', const=True, help='GOADB (Glyph order and alias database) to be used')
    addarg('-a', '--afm', nargs='?', const=True, help='AFM filename to be used')
    addarg('-m', '--math', nargs='*', help='MATH feature filename to be used')
    addarg('-x', '--extra',  nargs='*', help='Extra parameters to be set in OTF tables')
    addarg('-aa', '--aalt', action='store_true', help='Make a AALT feature')
    addarg('-ah', '--autohint', action='store_true', help='Auto hint all glyphs')
    addarg('-ac', '--autocorrect', action='store_true', help='Auto correct path (direction and atart points)')
    # ~ addarg('-v', '--validate', nargs='?', const=True, help='Output the report from font validation')
    addarg('-sf', '--savefea', nargs='?', const=True, help='Output the used features')
    addarg('-q', '--quiet', action='store_true', help='Less messages')

    args = argpars.parse_args()
    iname  = args.input.strip()
    # iname will be the path without extension:
    iname = re.sub(r'\.[^\.]+$', '', iname)
    # 22.01.2019 13:46:13:
    bname = os.path.basename(iname)
    # temporarily, 22.01.2019 13:41:10, before making it an argument:
    # input EPS directory:
    # 19.02.2019 23:57:45:
    edir = args.epsdir
    # ~ edir = 'srceps'
    # input EPS path (directory and basename) without extension:
    ename = os.path.join(edir, bname)
    oname  = args.output

    jgname  = args.jsongoadb
    joname  = args.jsonoti
    jfname  = args.jsonfont

    otiname  = args.oti
    temp_dir = args.tempdir



    tname  = args.typeone
    sname  = args.save
    fename = args.fea
    gname  = args.goadb
    afname = args.afm
    mtname = args.math
    extrapars = args.extra
    aalt   = args.aalt
    ahint  = args.autohint
    acorr  = args.autocorrect
    # ~ ovaname = args.validate
    ofename = args.savefea
    quiet  = args.quiet


    pydir = args.pydir

    # ------------------------------------------------------------------------------
    # prepare logging:

    # logging goes to the temp dir
    # (the logs will be appendet to the higher level logs)
    log_name = os.path.join(temp_dir, 'algotype_font_generation_log.txt')
    debug_name = os.path.join(temp_dir, 'algotype_font_generation_debug.txt')

    # start a log object, first removing the existing logs:
    log = log_lib.start_log(log_name=log_name, debug_name=debug_name,
        log_level='debug', screen_level='info', remove=True)


    
    
    
    # ------------------------------------------------------------------------------

    log_lib.info('starting Algotype Fontforge subprocess for', iname)

    # ------------------------------------------------------------------------------
    # from font_json to oti font and pfb font:

    font_json = lib.read_json(jfname)

    # put the information from font_json
    # to the fontforge font object:

    font = fontforge.font()
    # ~ log_lib.debug('font italic angle', font.italicangle)

    log_lib.info('writing font parameters')
    json_font_parameters_to_font(font_json['par'])

    log_lib.info('writing font glyphs')
    json_to_glyphs(font_json['glyphs'])

    # gly is a glyph identifier
    # collect all of them:
    glyphs_names_json = [gly for gly in font_json['glyphs']]

    gly_dic = dict([(g.glyphname, g) for g in font.glyphs()])

    glyphs_names_gly_dic = [gly for gly in gly_dic]

    # ordered list of fontforge glyphs:

    for gn in font_json['glyph_list']:
        if gn not in gly_dic:
            log_lib.debug('glyph %s not found in gly_dic' % gn)

    gly_lst = [gly_dic[n] for n in font_json['glyph_list'] if n in gly_dic]

    gly_lst_names = [g.glyphname for g in gly_lst]

    # compare lists of glyph names (for debugging purposes):

    def compare_sets(name_a, a, name_b, b):
        '''
        compare sets of glyph names
        and report the difference to the debug log,
        if the result is nonempty
        '''
        diff = set(a) - set(b)
        if len(diff) > 0:
            message = '[%s] minus [%s] = %s' % (name_a, name_b, str(list(diff)))
            log_lib.debug(message)
            
    compare_sets('glyphs_names_json', glyphs_names_json,
        'glyphs_names_gly_dic', glyphs_names_gly_dic)
    compare_sets('glyphs_names_gly_dic', glyphs_names_gly_dic,
        'glyphs_names_json', glyphs_names_json)
    compare_sets('gly_lst_names', gly_lst_names,
        'glyphs_names_gly_dic', glyphs_names_gly_dic)
    compare_sets('glyphs_names_gly_dic', glyphs_names_gly_dic,
        'gly_lst_names', gly_lst_names)

    # it seems they are equal

    log_lib.info('writing font encodings')
    set_encoding(font_json['encodings'])

    # reasonable state (uses indirect access to (items in) global font.glyphs():

    log_lib.info('writing kern data')
    kern_info_to_font(font_json['kerns'])

    # 05.03.2019 17:42:51:
    log_lib.info('writing font features')
    feature_strings_to_font(font_json['features'])

    log_lib.debug('aalt, accor, ahint:', aalt, acorr, ahint)

    # possibly make an AALT feature:
    if aalt:
        log_lib.info("regenerating AALT feature")
        font.buildOrReplaceAALTFeatures()

    # auto correct the direction of paths
    # using FontForge functions:
    if acorr:
        log_lib.info("auto correcting directions of paths")
        for n, g in gly_dic.items():
            g.correctDirection()
            if g.changed:
                log_lib.debug("%-20s paths corrected" % n)
            g.canonicalStart()

    # auto hint the font
    # using the FontForge function autoHint:
    if ahint:
        log_lib.info("auto hinting font")
        for n, g in gly_dic.items():
            g.autoHint()


    goadb = font_json['goadb']

    # rename glyphs based on the information just read:
    # why sometimes renaming is done three times?

    # turn off
    # 21.08.2019 01:39:37:
    # renaming info is generated inside the function rename_glyphs
    # ~ log_lib.info('renaming glyphs')
    rename_glyphs(goadb['alias'], goadb['unic'])

    # 24.02.2019 21:03:38
    # a phase of cleaning stopped here

    if extrapars:
        log_lib.info('setting extra font parameters')
        set_extrapars(extrapars)

    calculate_private_dict()

    if ofename:
        ofename = ofename.strip()
        log_lib.info("FEA > %s" % ofename)
        font.generateFeatureFile(ofename)

    # unconditionally, as of 20.04.2020 23:06:02:
    validate_font()

    # genarating sfd moved from here to -- after generating otf
    # 11.03.2020 16:36:38

    if 1:
        if tname:
            tname = tname.strip()
            if (tname=='*'):
                tname = font.fontname + '_T1' + '.pfb'
            rename_glyphs(goadb['xalias'])
            log_lib.info("Type1 > %s" % tname)
            font.generate(tname, flags=('afm', 'pfm',))
            log_lib.info('renaming Type1 glyphs')
            rename_glyphs(goadb['alias'])
            oti_fnt = font_json['oti_par']
            log_lib.info('fixing AFM file generated by Fontforge (will be replaced, anyway)')
            fix_afm(tname.replace('.pfb', '.afm'), oti_fnt)
            log_lib.info('fixing PFB file generated by Fontforge')
            fix_pfm(tname.replace('.pfb', '.pfm'), oti_fnt)

    if oname:
        # temporarily not removing, untill it is reprogrammed
        # 21.08.2019 01:35:48:
        remove_redundant_glyphs(goadb)
        oname = oname.strip()
        if (oname=='*'):
            oname = font.fontname + '_OT' + '.otf'
        log_lib.info("OTF > %s" % oname)
        font.generate(oname, flags=('opentype',))

    if sname:
        if sname == True:
            sname = iname + '.sfd'
        sname = sname.strip()
        log_lib.info("SFD > %s" % sname)
        font.save(sname)
        # font.saveNamelist(iname + '.nam')
        # AVOID core dump with ligatures (reopen font):
        # font.close()
        # font = fontforge.open(sname)

    font.close()
    
    # finally flush the info in the log files:
    
    log.log_file_flush()
    log.debug_file_flush()


if __name__ == '__main__':
    main()"""
ff_make_font_str3 = r"""#!/usr/bin/python
# -*- coding: utf-8 -*-

# make parts of the file both Python 2 and Python 3 compatible

'''
ff_make_font
FontForge make font
17.03.2020 17:16:56

previously (in Metatype1) known as FFDKM:
(FFDKM was "Python FontForge based Developement Kit for Metatype1")

A converter of METAPOST glyphs into Type1 and OpenType (CFF).
Includes advanced OpenType features and math functionality.

'''

__author__ = "Piotr Strzelczyk, Marek Ryćko and Bogusław Jackowski"
__copyright__ = "Copyright (c) 2017, 2020 by GUST e-foundry"
__credits__ = ["Piotr Strzelczyk", 'Marek Ryćko', "Bogusław Jackowski", "Piotr Pianowski"]
__license__ = "GPL"
__maintainer__ = 'Marek Ryćko'
__email__ = "marek@do.com.pl"
__status__ = "Beta"

# python standard library:
import os.path
import sys
import string
import re
import gc
from argparse import ArgumentParser
# json module for serialization of structures
import json

# Algotype library:
from . import at_lib as lib
from . import log_lib

# ReportLab PFM library; part of the ReportLab PDF Toolkit:
# (possibly in the form adaptede to Python3 by Marek Ryćko
from .pfm import PFM

# FontForge python bindings:
# logging, using log_lib, is not yet possible;
# we are before reading arguments
try:
    import fontforge
except ImportError:
    # ~ log_lib.critical(u'FontForge must be compiled with --pyextension.')
    sys.exit('FontForge must be compiled with --pyextension.')
if not hasattr(fontforge, 'math'):
    # ~ log_lib.critical(u'Too old FontForge — doesn’t support MATH table.')
    sys.exit('Too old FontForge — doesn’t support MATH table.')

# ------------------------------------------------------------------------------
# to further library:
# ------------------------------------------------------------------------------
def write_file(s, fn, mess):
    '''
    create a file of a filename fn
    write a string s to this file in a text mode
    and display a critical error message in case of error
    '''
    try:
        # create a file handler:
        fh = open(fn, 'w')
    except IOError:
        log_lib.critical(mess + ': %s' % fn)

    fh.write(s)
    fh.close()

# ------------------------------------------------------------------------------
# reading data from a json font file
# and storing it in a font generated by some engine
# (fontforge as of 01.04.2019 13:03:19)
# ------------------------------------------------------------------------------




# ------------------------------------------------------------------------------
# setting metainformation (global parameters) of the font:
# ------------------------------------------------------------------------------

    
    
def json_font_parameters_to_font(par):
    '''
    read a dictionary (a json structure) of font parameters
    and put it into a fontforge font structure
    font is a global variable (so far)
    '''

    def set_names(names):
        # ~ log_lib.debug('names', names)
        for l, d in list(names.items()):
            for i in d:
                # ~ font.appendSFNTName(l, i, d[i])
                # 19.08.2019 19:45:22:
                # after serialization and deserialization to and from json
                # the l and i values were unicode instead of string
                # ~ if str(l).lower() in ('ascender', 'capheight'):
                # ~ log_lib.debug('Setting SFNT table in FontForge font', str(l), str(i), d[i])
                font.appendSFNTName(str(l), str(i), d[i])

    def set_attributes(attr):
        for a, v in list(attr.items()):
            try:
                log_lib.debug('Setting font attribute in FontForge font %s: %s' \
                    % (str(a), str(v)))
                setattr(font, a, v)
            except:
                # the nonexistent attributes are almost silently skipped:
                message = 'It’s OK, that we do not set the (nonexisting) font attribute: %s' % a
                log_lib.debug(message)

    # --------------------------------------------------------------------------
    # writing:

    # constant for Algotype:
    font.em = par['em']

    # write information from names and attr dictionaries
    # to the FontForge font object:
    # ~ log_lib.debug(par['names'])
    set_names(par['names'])
    set_attributes(par['attr'])
    
    # "ASCENDER": "694.44444"
    # ~ log_lib.debug('font.ascent', font.ascent)
    # ~ font.ascent = 695.55555
    # ~ log_lib.debug('changed font.ascent to', font.ascent)

    font.sfntRevision = par['revision']
    
    if par['pan'] is not None:
        font.os2_panose = tuple(par['pan'])

    # write oti font bold and italic attributes to the FontForge font structure:

    # ~ log_lib.debug('stylemap', font.os2_stylemap)
    # result: 0
    # ~ log_lib.debug('weight', font.os2_weight)
    # result: 400
    
    ff_bold = 32
    ff_bold_weight = 700
    ff_italic = 1
    ff_regular = 64
    
    if par['bold']:
        font.os2_weight = ff_bold_weight
        font.os2_stylemap |= ff_bold

    if par['italic']:
        font.os2_stylemap |= ff_italic
        
    # PSt: why < 1 ?
    if font.os2_stylemap < 1:
        font.os2_stylemap = ff_regular    
    
# ------------------------------------------------------------------------------
# glyphs to encoding:
# ------------------------------------------------------------------------------


def encoding_structure_to_string(encd):
    '''
    MR, 24.02.2019 13:48:49
    partially based on PSt’s function set_encoding.
    take an encoding structure, based on oti_gly structure
    and serialize it as a string
    to be further written to a file
    and input to fontforge
    '''
    enc = encd['enc']
    encname = encd['encname']

    # string list sl (line list):
    sl = []

    # generate the lines:
    sl.append('/%s[' % encname)
    for i in range(256):
        sl.append('/%s' % enc[i])
    sl.append('] def')
    
    # join lines making the string:
    s = '\n'.join(sl)
    # ~ log_lib.debug(s)
    return s

def set_encoding(es):
    '''
    this set_encoding function
    and the encoding name encname
    from the encoding structure es
    prepared from oti_gly (part of structure read from oti file)
    
    it is a refactored version of set_encoding by Piotr Strzelczyk, PSt
    refactoring by MR
    on 24.02.2019 14:27:09
    '''
    
    s = encoding_structure_to_string(es)

    # ~ fn = iname + '_PFB.enc'
    # 24.06.2019 23:33:29:
    fn = iname + '_pfb.enc'
    mess = "Couldn't create ENC file"
    # temp file for fontforge:
    write_file(s, fn, mess)
        
    fontforge.loadEncodingFile(fn)
    encname = es['encname']
    font.encoding = encname
    # cleaning up:
    # ~ os.remove(fn)


# ------------------------------------------------------------------------------
# including adobe feature files (as strings) to the font:
# ------------------------------------------------------------------------------

def feature_strings_to_font(features):
    '''
    read features, a list of strings
    each representing an adobe feature file
    and put them to the fontforge font
    
    '''
    # ~ log_lib.debug('features as a list:', features)
    for fs in features:
        # fs is a feature string
        # write it to a temporary file
        # and put into the font
        # write feature string to a temporary file:
        
        # temp_dir is already created, by oti_to_font
        fea_path = os.path.join(temp_dir, 'feature.fea')
        try:
            fh = open(fea_path, 'w')
            fh.write(fs)
            fh.close()
            font.mergeFeature(fea_path)
        except EnvironmentError as IOError:
            log_lib.error("Couldn't find FEA file: %s" % fnm)

# ------------------------------------------------------------------------------


def fix_afm(afmname, oti):
    try:
        frafm = open(afmname, 'r')
    except IOError:
        log_lib.critical("Couldn't read (created) AFM file: %s" % afmname)
    AFMT = []
    for line in frafm.readlines():
        AFMT.append(line.rstrip())
    frafm.close()
    for i in range(len(AFMT)):
        if 'StartCharMetrics' in AFMT[i]:
            com_ins=i
        if '; L' in AFMT[i]:
            AFMT[i]=remove_ligatures_dup(AFMT[i])
    AFMT[com_ins:com_ins] = afm_tfm_comments(oti)
    try:
        fwafm = open(afmname, 'w')
    except IOError:
        log_lib.critical("Couldn't write AFM file: %s" % afmname)
    for l in AFMT:
      fwafm.write(l + '\n')
    fwafm.close()

def afm_tfm_comments(oti):
    '''
    a maintained copy of this function is now in afm_lib
    this functions’s existence here will become obsolete
    '''
    res = []
    if 'PFM_NAME' in oti:
        res.append('Comment PFM parameters: %s %s %s %s' % (oti['PFM_NAME'], 
          oti['PFM_BOLD'], oti['PFM_ITALIC'], oti['PFM_CHARSET']))
    if 'DESIGN_SIZE' in oti:
        res.append('Comment TFM designsize: %s (in points)' % (oti['DESIGN_SIZE']))
    if 'FONT_DIMEN' in oti:
        fd=oti['FONT_DIMEN']
        fn=oti['DIMEN_NAME']
        for i in range(256):
            s=str(i)
            if s in fd:
                res.append('Comment TFM fontdimen %2s: %-10s %s' % (s, fd[s], fn[s]))
    if 'HEADER_BYTE' in oti:
        hb=oti['HEADER_BYTE']
        for i in ('9', '49', '72'):
            if i in hb:
                res.append('Comment TFM headerbyte %2s: %s' % (i, hb[i]))
    return res

def fix_pfm(pfmname, oti):
    try:
        pfm = PFM(pfmname)
    except IOError:
        log_lib.critical("Couldn't read (created) PFM file: %s" % pfmname)
        return
    if 'PFM_CHARSET' in oti:
        pfm.dfCharSet = int(oti['PFM_CHARSET'], 16)
    if 'PFM_ITALIC' in oti:
        # ~ log_lib.debug("oti['PFM_ITALIC']", oti['PFM_ITALIC'])
        if pfm.dfItalic != int(oti['PFM_ITALIC']):
           log_lib.warning("Bad Italic bit in result PFM file: %s" % pfmname)
    if 'PFM_BOLD' in oti:
        if (pfm.dfWeight > 500) != int(oti['PFM_BOLD']):
          log_lib.warning("Bad Weight info in result PFM file: %s" % pfmname)
    pfm.write_to_file(pfmname)
    
def remove_ligatures_dup(afl):
    src=afl.split(';')
    res=[]
    ligs={}
    for f in src:
        if f not in ligs:
            res.append(f)
            ligs[f]=1
    return ';'.join(res)

# ------------------------------------------------------------------------------
# glyph outlines:
# ------------------------------------------------------------------------------

def kern_info_to_font(kerns):
    '''
    take a json kerns structure
    and put the kerns into the fontforge font structure
    font and gly_dic are global substructures within fontforge
    '''

    font.addLookup('kerns', 'gpos_pair', (), (("kern", (("DFLT", ("dflt",)),("latn", ("dflt",)))),) )
    font.addLookupSubtable('kerns', 'kerns0')

    for gly, inf in list(kerns.items()):
        # ~ log_lib.debug(gly, inf)
        # inf is a dictionary of kerns (from glyph names to int kern values)
        glyph = gly_dic[gly]
        for g, val in list(inf.items()):
            # ~ glyph.addPosSub('kerns0', g, val)
            # 12.10.2019 20:09:25:
            # val can be any number, especially int or float:
            glyph.addPosSub('kerns0', g, int(round(val)))


# ------------------------------------------------------------------------------
# glyph outlines:
# ------------------------------------------------------------------------------


def json_to_glyphs(gj):
    '''
    write a json glyph structure (a dictionary of single json glyphs)
    to a fontforge font structure
    '''
    
    # ~ paths_source = 'eps'
    paths_source = 'json'
    
    for gly, g in list(gj.items()):
        # gly is a glyph identifier
        # g is a single glyph json structure
        # ~ log_lib.debug('generating [' + gly + ', ' + str(g['codepoint']) + ']')
        codepoint = -1 if g['codepoint'] is None else g['codepoint']
        # ~ log_lib.debug('generating [' + gly + ', ' + str(codepoint) + ']')
        # ~ log_lib.debug(str(g['eps']))
        
        # codepoint may be -1, -10 or a positive value
        if codepoint != -10:
            # the glyph not to be skipped
            
            glyph = font.createChar(codepoint, gly)

            if 0:
                # old code:

                # write eps info to the fontforge glyph:
                if g['eps'] is not None:
                    # too small eps strings are equivalent to empty:
                    if len(g['eps']) > 180:
                        if paths_source == 'eps':
                            # 1.
                            # write eps to a temporary file:
                            eps_path = os.path.join(temp_dir, 'glyph.eps')
                            fh = open(eps_path, 'w')
                            fh.write(g['eps'])
                            fh.close()
                            # 2. write the paths in eps to the glyph:
                            try:
                                glyph.importOutlines(eps_path)
                            except:
                                log_lib.error("Cannot import outline for glyph:\n  %s" % gly)
                        elif paths_source == 'json':
                            # create a fontforge glyph path info
                            # in the glyph element of a fontforge font
                            # from a structural information from a json structure:
                            json_to_glyph(g, glyph)
                        else:
                            # no other sources are implemented now:
                            pass
                        glyph.correctDirection()
                        glyph.canonicalStart()
                        glyph.canonicalContours()
                    else:
                        glyph.changed=True
                        pass
                else:
                    # ~ log_lib.warning("Missing EPS info in OTI for glyph:\n  %s" % gly)
                    pass

            else:
                # new code, as of 10.12.2019 21:46:56:
                
                
                # write eps info to the fontforge glyph:
                if 'paths' in g:
                    # empty paths are not written:
                    if len(g['paths']['us']) > 0:
                        if paths_source == 'eps':
                            # 1.
                            # write eps to a temporary file:
                            eps_path = os.path.join(temp_dir, 'glyph.eps')
                            fh = open(eps_path, 'w')
                            fh.write(g['eps'])
                            fh.close()
                            # 2. write the paths in eps to the glyph:
                            try:
                                glyph.importOutlines(eps_path)
                            except:
                                log_lib.warning("Cannot import outline for glyph:\n  %s" % gly)
                        elif paths_source == 'json':
                            # create a fontforge glyph path info
                            # in the glyph element of a fontforge font
                            # from a structural information from a json structure:
                            json_to_glyph(g, glyph)
                        else:
                            # no other sources are implemented now:
                            pass
                        glyph.correctDirection()
                        glyph.canonicalStart()
                        glyph.canonicalContours()
                    else:
                        glyph.changed=True
                        pass
                else:
                    # ~ log_lib.warning("Missing EPS info in OTI for glyph:\n  %s" % gly)
                    pass

            # write metrical info to the fontforge glyph:
            # moved after putting path info to the gliph on 25.09.2019 22:08:25:
            m = g['metrics']
            if 'width' in m:
                glyph.width = m['width']
                # experiment, 14.10.2019 14:54:25:
                # ~ glyph.width = 888.777
            if 'textheight' in m:
                glyph.texheight = m['textheight']
            if 'textdepth' in m:
                glyph.texdepth = m['textdepth']


        else:
            pass
            log_lib.debug('not generating (skipping) [' + gly + ', ' + str(codepoint) + ']')



def json_to_glyph(g, glyph):
    '''
    create a fontforge glyph path info
    in the glyph element of a fontforge font
    from a structural information from a json structure
    '''
    pen = glyph.glyphPen()

    # ~ grammar_data = [
        # ~ ['setrgbcolor', 3],
        # ~ ['newpath', 0],
        # ~ ['moveto', 2],
        # ~ ['lineto', 2],
        # ~ ['curveto', 6],
        # ~ ['lineto', 2],
        # ~ ['closepath', 0],
        # ~ ['fill', 0],
        # ~ ['showpage', 0],
    # ~ ]
    
    commands = g['paths']['us']
    
    for com in commands:
        # execute a fontforge counterpart of a command
        f = com['t']
        x = com['v']
        if f in ('setrgbcolor', 'setgray', 'fill', 'showpage'):
            pass
        if f in ('newpath',):
            pass
        elif f == 'moveto':
            pen.moveTo((x[0], x[1]))
        elif f == 'lineto':
            pen.lineTo((x[0], x[1]))
        elif f == 'curveto':
            pen.curveTo((x[0], x[1]), (x[2], x[3]), (x[4], x[5]), )
        elif f == 'closepath':
            pen.closePath()
        else:
            pass

# ------------------------------------------------------------------------------



def prepare_OS2(attr, n, v):
#      os2_version = 5
#    + FSType <number>;            os2_fstype
#    + Panose <panose number>;     os2_panose
#    - UnicodeRange <Unicode range list>;  os2_unicoderanges
#    - CodePageRange <code page list>;  os2_codepages
#    + TypoAscender <metric>;      os2_typoascent, os2_typoascent_add
#    + TypoDescender <metric>;     os2_typodescent, os2_typodescent_add
#    + TypoLineGap <metric>;       os2_typolinegap
#    + winAscent <metric>;         os2_winascent, os2_winascent_add
#    + winDescent <metric>;        os2_windescent, os2_windescent_add
#    - XHeight <metric>;           -- readonly in FF
#    - CapHeight <metric>;         -- readonly in FF
#    + WeightClass <number>;       +- os2_weight
#    + WidthClass <number>;        +- os2_width
#    + Vendor <string>;            os2_vendor
#    ? LowerOpSize <number>;
#    ? UpperOpSize <number>;
#   -- AvgCharWidth     
#      SubscriptXSize              os2_subxsize
#      SubscriptYSize          os2_subysize
#      SubscriptXOffset        os2_subxoff
#      SubscriptYOffset        os2_subyoff
#      SuperscriptXSize        os2_supxsize
#      SuperscriptYSize        os2_supysize
#      SuperscriptXOffset      os2_supxoff
#      SuperscriptYOffset      os2_supyoff
#      StrikeoutSize               os2_strikeysize
#      StrikeoutPosition       os2_strikeypos
#   -- sFamilyClass                os2_family_class
#      fsSelection  
#          0    bit 1   ITALIC     Font contains italic or oblique characters.
#          1        UNDERSCORE Characters are underscored.
#          2        NEGATIVE   Characters have their foreground and background reversed.
#          3        OUTLINED   Outline (hollow) characters, otherwise they are solid.
#          4        STRIKEOUT  Characters are overstruck.
#          5    bit 0   BOLD       Characters are emboldened.
#          6        REGULAR    Characters are in the standard weight/style for the font.
#          7 os2_use_typo_metrics        USE_TYPO_METRICS If set, it is strongly recommended to use
#                                  OS/2.sTypoAscender - OS/2.sTypoDescender+ OS/2.sTypoLineGap
#                                  as a value for default line spacing for this font.
#          8 os2_weight_width_slope_only WWS The font has ‘name’ table strings consistent with
#                                  a weight/width/slope family without requiring use of ‘name’
#                                  IDs 21 and 22.
#   -- DefaultChar  
#      BreakChar    
#      MaxContext
    OS2fields = {
       'SubscriptXSize'   : 'os2_subxsize',
       'SubscriptYSize'   : 'os2_subysize',
       'SubscriptXOffset' : 'os2_subxoff',
       'SubscriptYOffset' : 'os2_subyoff',
       'SuperscriptXSize' : 'os2_supxsize',
       'SuperscriptYSize' : 'os2_supysize',
       'SuperscriptXOffset': 'os2_supxoff',
       'SuperscriptYOffset': 'os2_supyoff',
       'StrikeoutSize'     : 'os2_strikeysize',
       'StrikeoutPosition' : 'os2_strikeypos',
    }
    if n in OS2fields:
        attr[OS2fields[n]] = int(v)


def set_variants(vari):
    for ch, t, hv, rest in vari:
        try:
            gl = gly_dic[ch]
        except KeyError:
            log_lib.warning("Glyphname %s (used in math parameters) absent from font" % ch)
            continue
        if t == 'var':
            ls = rest.split()
            lss = []
            if ls[0] != ch:
                lss.append(gl.glyphname)
            for c in ls:
                if c in gly_dic:
                    lss.append(gly_dic[c].glyphname)
                else:
                    log_lib.warning("Glyphname %s (used in math parameters) absent from font" % c)
            lss = ' '.join(lss) # must be glyphs NOT glyphs name!
            # log_lib.debug(lss)
            if hv == 'h':
                gl.horizontalVariants = lss
            else:
                gl.verticalVariants = lss
        elif t == 'ext':
            r = re.sub(' *}', '}', re.sub(' *{ *', '{', re.sub(' *, +', ',', rest)))
            ls = r.split()
            lss = []
            for c in ls:
                m = re.search(r'([A-Za-z0-9_\.]+){([0-1]),([0-9]+),([0-9]+),([0-9]+)}', c)
                if m:
                    cc = m.group(1)
                    if cc in gly_dic:
                        lss.append((gly_dic[cc], m.group(2) == '1',
                           int(m.group(3)), int(m.group(4)), int(m.group(5))))
                else:
                    log_lib.error("Invalid format of extension data: %s" % c)
            #log_lib.debug(lss)
            if hv == 'h':
                gl.horizontalComponents = lss
            else:
               gl.verticalComponents  = lss

def set_itcor(itcor):
    for ch, t, v in itcor:
        if ch in gly_dic:
            if t == 'ext':
                if font[ch].verticalComponents:
                     font[ch].verticalComponentItalicCorrection = int(v)
                elif font[ch].horizontalComponents:
                     font[ch].horizontalComponentItalicCorrection = int(v)
                else:
                    log_lib.warning("Extension italic correction set for glyph %s, without components" % ch)
            else:
                font[ch].italicCorrection = int(v)
        else:
            log_lib.warning("Glyphname %s (used in math accent_axes) absent from font" % ch)

def set_vertex(verx):
    for ch, t, w in verx:
        if ch in gly_dic:
            v = w.split()
            v.append('29999')
            l = len(v)
            if l < 4 or l % 2 > 0:
                log_lib.error("Missformed math kern line for glyph %s" % ch)
            tt = tuple([(int(v[2*i]), int(v[2*i+1])) for i in range(l/2)])
            # tt = tuple(zip(*[iter(v)]*2))
            p = -29999
            for v, h in tt:
                if h<p:
                    log_lib.error("Missformed math kern line for glyph %s" % ch)
                p = h
            if p != 29999:
                log_lib.error("Missformed math kern line for glyph %s" % ch)
            # log_lib.debug(tt)
            if t == 'ur':
                font[ch].mathKern.topRight = tt
            elif t == 'ul':
                font[ch].mathKern.topLeft = tt
            elif t == 'lr':
                font[ch].mathKern.bottomRight = tt
            elif t == 'll':
                font[ch].mathKern.bottomLeft = tt
            else:
                log_lib.warning("Unknown type of math kern: %4s in %s" % (t, ch))
        else:
            log_lib.warning("Glyphname %s (used in math kerning) absent from font" % ch)

def set_axis(axi):
    for ch, v in axi:
        if ch in gly_dic:
            font[ch].topaccent = int(v)
        else:
            log_lib.warning("Glyphname %s (used in math accent_axes) absent from font" % ch)

def set_extend(ext):
    for ch in ext:
        if ch in gly_dic:
            font[ch].isExtendedShape = True
        else:
            log_lib.warning("Glyphname %s (used in math is_extented) absent from font" % ch)

def set_extrapars(xpars):
    for xp in xpars:
        m = re.search(r'^(.+) *[=#] *(.+)$', xp)
        if m and m.group(1) == 'use_typo_metrics':
           if m.group(2) in ('0','1'):
               font.os2_use_typo_metrics = int(m.group(2))
           else:
               log_lib.error("Inproper value of use_typo_metrics: %s" % m.group(2))
        elif m and m.group(1) == 'set_ps_names':
           if m.group(2) == '1':
               copy_ttf_to_ps_names();
           elif m.group(2) != '0':
               log_lib.error("Inproper value of set_ps_names: %s" % m.group(2))
        elif m:
           log_lib.warning("Unrecognised extra parametr: %s" % m.group(1))
        else:
           log_lib.error("Invalid format of extra parametr: %s" % xp)


def copy_ttf_to_ps_names():
    for t in font.sfnt_names:
        if t[1]=='Copyright':
             font.copyright=t[2]
        if t[1]=='Family':
             font.familyname=t[2]
        if t[1]=='SubFamily':
             pass
        if t[1]=='Fullname':
             font.fullname=t[2]
        if t[1]=='PostScriptName':
             font.fontname=t[2] # always the same as Fullname?
    # font.version
    # font.sfntRevision = round(float(font.version)*65536)/65536

def calculate_private_dict():
    priv=font.private
    for ent in ['BlueValues', 'OtherBlues', 'StdHW', 'StdVW', 
      'StemSnapH', 'StemSnapV', 'BlueShift', 'BlueScale']:
        priv.guess(ent)
    if len(priv['BlueValues'])>1 and priv['BlueValues'][1]!=0: # first have to be baseline
        log_lib.debug("Correcting Blue values")
        bv=[v for v in priv['BlueValues']]
        bv[1]=0
        priv['BlueValues']=tuple(bv)
    # corect language tuple of 'kern' feature:
    kern_slt=None
    for ln in font.gsub_lookups:
        l_t, l_f, feat_slt = font.getLookupInfo(ln)
        if len(feat_slt) and feat_slt[0][0]=='salt':
            kern_slt=(('kern',feat_slt[0][1]),)
    if kern_slt:
        font.lookupSetFeatureList('kerns',kern_slt)
        
        
# ------------------------------------------------------------------------------
# renaming glyphs in the font
# according to goadb info:
# ------------------------------------------------------------------------------

def rename_glyphs(alias, unic=None):
    # if unic != None it is main name change and unicode numbering,
    # else it is only name for Type1 change
    #
    # below byway due to `glyphnameIsComponent()'
    # used by .glyphname to find associated names
    
    def sanit(n):
        return re.sub(r'\.','!!!',n)
    def tinas(n):
        return re.sub(r'!!!','.',n)

    if unic:
        log_lib.info('renaming glyphs')
        # no counting steps, as of 15.12.2019 22:44:44:
        # ~ log_lib.info("GLYPH rename: 1")
        # made even more quiet, 11.04.2019 00:06:40:
        # log_lib.debug("almost done")
    for g in gly_lst:
        if '.' in g.glyphname:
            g.glyphname = sanit(g.glyphname)

    if unic:
        # 15.12.2019 22:45:04:
        # ~ log_lib.debug("  2")
        pass
    for n, g in list(gly_dic.items()):
        if unic:
            if n in alias:
                if n != alias[n]:
                    g.glyphname = sanit(alias[n])
                if n in unic:
                    ffunic = g.unicode
                    if  ffunic != unic[n] and unic[n] != -10:
                        if ffunic > 0 and unic[n] < 0:
                            log_lib.warning("%-20s %04x unicode not in GOADB" % (n, ffunic))
                        elif ffunic < 0 and unic[n] > 0:
                            pass # irrelevant info
                            # log_lib.warning("%-20s %04x unicode not in FF" % (n, unic[n]))
                        elif ffunic > 0 and unic[n] > 0:
                            log_lib.warning("%-20s %04x in GOADB, %04x in FF" % (n, unic[n], ffunic))
                        else:
                            log_lib.error("%-20s can't happen" % n)
                        g.unicode = unic[n]
            else:
                if g.unicode > 0:
                    log_lib.warning("%-20s %04x not in GOADB" % (n, g.unicode))
                else:
                    log_lib.warning("%-20s not in GOADB" % n)
        else:
            n = tinas(g.glyphname) # `current' glyphname
            if n in alias and n != alias[n]:
                g.glyphname = sanit(alias[n])
                    
    if unic:
        # 15.12.2019 22:45:18:
        # ~ log_lib.debug("  3")
        pass
    for g in gly_lst:
        if '!!!' in g.glyphname:
           g.glyphname = tinas(g.glyphname)

    if unic:
        # 15.12.2019 22:45:35:
        # ~ log_lib.debug("  4 -- done")
        pass

def remove_redundant_glyphs(goadb):
    for k, v in list(gly_dic.items()):
        # ~ log_lib.debug('considering for removal (old name %s)' % k)
        if k in goadb['unic']:
            # ~ log_lib.debug('considering for removal (old name %s): %s' % (k, goadb['alias'][k]))
            if goadb['unic'][k] == -10:
                # ~ log_lib.debug('key:', k, 'unic of key:', goadb['unic'][k], 'alias of key:', goadb['alias'][k])
                if 0:
                    log_lib.debug('glyph to be removed (old name %s): %s' % (k, goadb['alias'][k]))
                # ~ font.removeGlyph(goadb['alias'][k])
                # 19.08.2019 19:47:47:
                # if goadb['alias'][k] was unicode, the fontforge asked for an integer:
                # the glyph to be skipped was not put to the font earlier, so there is
                # no need to remove it:
                try:
                    font.removeGlyph(str(goadb['alias'][k]))
                except:
                    log_lib.error('failed removing glyph %s from the font' % str(goadb['alias'][k]))
                
# ------------------------------------------------------------------------------


def validate_font():
    warn = []
    def addwarn(w, v, m, s):
        if v&m:
            if s:
                if len(w): w.append(', %s' % s)
                else: w.append('%s' % s)
            return v - m
        else:
            return v
    font.validate(1)
    for n, g in list(gly_dic.items()):
        if g.validation_state > 1:
            v = g.validation_state
            w = []
            v=addwarn(w, v, 0x1, None)
            v=addwarn(w, v, 0x2, 'open contour')
            v=addwarn(w, v, 0x4, 'contours intersections')
            v=addwarn(w, v, 0x8, 'wrong direction of contour')
            v=addwarn(w, v, 0x200, 'invalid glyph name')
            v=addwarn(w, v, 0x100000, 'missing anchor')
            v=addwarn(w, v, 0x200000, 'duplicate glyph name')
            v=addwarn(w, v, 0x400000, 'duplicate unicode')
            v=addwarn(w, v, 0x20, None) # 'missing extrema in path'
            v=addwarn(w, v, 0x80, 'too many points in glyph')
            v=addwarn(w, v, 0x100, 'too many hints in glyph')
            v=addwarn(w, v, 0x40000, 'points toofar apart')
            if v > 0: w.append(', unrecognized warning: %x' % v)
            if len(w):
                 warn.append('%-20s' % (n + ':'))
                 warn.extend(w)
                 warn.append('\n')
    v = font.privateState    
    w = []
    v=addwarn(w, v, 0x1, 'odd number of elements in Blue')
    v=addwarn(w, v, 0x2, 'elements in Blue are disordered')
    v=addwarn(w, v, 0x4, 'too many elements in Blue')
    v=addwarn(w, v, 0x8, 'elements in Blue are too close')
    v=addwarn(w, v, 0x10000, 'missing BlueValues')
    v=addwarn(w, v, 0x20000, 'bad BlueFuzz')
    v=addwarn(w, v, 0x40000, 'bad BlueScale')
    if v > 0: w.append(', unrecognized warning: %x' % v)
    if len(w):
         warn.append('%-20s' % ('Private:'))
         warn.extend(w)
         warn.append('\n')
         
    # prepare the warning multiline string
    if len(warn) == 0:
        warn.append('No warnings found')
    warning_string = '\n'.join(warn)
    # write the multiline string:
    log_lib.warning(warning_string)
    # not writing the warnings to a special file, separate from logs
    # as of 20.04.2020 23:04:31
    

# ------------------------------------------------------------------------------
# Start of processing:
# ------------------------------------------------------------------------------



# ~ font = None
# ~ gly_dic = None
# ~ gly_lst = None


# ~ iname
# ~ bname
# ~ edir
# ~ ename
# ~ oname
# ~ jgname
# ~ joname
# ~ jfname
# ~ otiname
# ~ temp_dir
# ~ tname
# ~ sname
# ~ fename
# ~ gname
# ~ afname
# ~ mtname
# ~ extrapars
# ~ aalt
# ~ ahint
# ~ acorr
# ~ ovaname
# ~ ofename
# ~ quiet
# ~ pydir













def main():

    # awful global variables; the remainder after old Metatype1; sorry
    # to be cleaned up in the fututre, as of 18.03.2020 22:41:54

    global font
    global gly_dic
    global gly_lst
    
    
    global iname
    global bname
    global edir
    global ename
    global oname
    global jgname
    global joname
    global jfname
    global otiname
    global temp_dir
    global tname
    global sname
    global fename
    global gname
    global afname
    global mtname
    global extrapars
    global aalt
    global ahint
    global acorr
    global ovaname
    global ofename
    global quiet
    global pydir

    # ------------------------------------------------------------------------------
    
    

    # ------------------------------------------------------------------------------
    # reading arguments:
    # ------------------------------------------------------------------------------
    argpars = ArgumentParser(description='Algotype: Type1 or OpenType converter',
         fromfile_prefix_chars='@')
    addarg=argpars.add_argument
    addarg('input', help='Input Algotype filename')
    # 20.02.2019 00:41:15:
    addarg('-e', '--epsdir', nargs='?', const=False, help='Directory for input EPS files')
    addarg('-p', '--pydir', nargs='?', const=False, help='Directory for Python input files')
    addarg('-o', '--output', nargs='?', const=False, help='Generated OTF file')
    addarg('-te', '--tempdir', nargs='?', const=False, help='Temporary directory')
    addarg('-oti', '--oti', nargs='?', const=False, help='Oti file')
    addarg('-jg', '--jsongoadb', nargs='?', const=False, help='Json goadb file')
    addarg('-jo', '--jsonoti', nargs='?', const=False, help='Json oti file')
    addarg('-jf', '--jsonfont', nargs='?', const=False, help='Json font file')
    addarg('-t', '--typeone', nargs='?', const=False, help='Generated Type1 file')
    addarg('-s', '--save', nargs='?', const=True, help='Output saved in sfd format')
    addarg('-f', '--fea', nargs='*', help='Feature filename to be used')
    addarg('-g', '--goadb',  nargs='?', const=True, help='GOADB (Glyph order and alias database) to be used')
    addarg('-a', '--afm', nargs='?', const=True, help='AFM filename to be used')
    addarg('-m', '--math', nargs='*', help='MATH feature filename to be used')
    addarg('-x', '--extra',  nargs='*', help='Extra parameters to be set in OTF tables')
    addarg('-aa', '--aalt', action='store_true', help='Make a AALT feature')
    addarg('-ah', '--autohint', action='store_true', help='Auto hint all glyphs')
    addarg('-ac', '--autocorrect', action='store_true', help='Auto correct path (direction and atart points)')
    # ~ addarg('-v', '--validate', nargs='?', const=True, help='Output the report from font validation')
    addarg('-sf', '--savefea', nargs='?', const=True, help='Output the used features')
    addarg('-q', '--quiet', action='store_true', help='Less messages')

    args = argpars.parse_args()
    iname  = args.input.strip()
    # iname will be the path without extension:
    iname = re.sub(r'\.[^\.]+$', '', iname)
    # 22.01.2019 13:46:13:
    bname = os.path.basename(iname)
    # temporarily, 22.01.2019 13:41:10, before making it an argument:
    # input EPS directory:
    # 19.02.2019 23:57:45:
    edir = args.epsdir
    # ~ edir = 'srceps'
    # input EPS path (directory and basename) without extension:
    ename = os.path.join(edir, bname)
    oname  = args.output

    jgname  = args.jsongoadb
    joname  = args.jsonoti
    jfname  = args.jsonfont

    otiname  = args.oti
    temp_dir = args.tempdir



    tname  = args.typeone
    sname  = args.save
    fename = args.fea
    gname  = args.goadb
    afname = args.afm
    mtname = args.math
    extrapars = args.extra
    aalt   = args.aalt
    ahint  = args.autohint
    acorr  = args.autocorrect
    # ~ ovaname = args.validate
    ofename = args.savefea
    quiet  = args.quiet


    pydir = args.pydir

    # ------------------------------------------------------------------------------
    # prepare logging:

    # logging goes to the temp dir
    # (the logs will be appendet to the higher level logs)
    log_name = os.path.join(temp_dir, 'algotype_font_generation_log.txt')
    debug_name = os.path.join(temp_dir, 'algotype_font_generation_debug.txt')

    # start a log object, first removing the existing logs:
    log = log_lib.start_log(log_name=log_name, debug_name=debug_name,
        log_level='debug', screen_level='info', remove=True)


    
    
    
    # ------------------------------------------------------------------------------

    log_lib.info('starting Algotype Fontforge subprocess for', iname)

    # ------------------------------------------------------------------------------
    # from font_json to oti font and pfb font:

    font_json = lib.read_json(jfname)

    # put the information from font_json
    # to the fontforge font object:

    font = fontforge.font()
    # ~ log_lib.debug('font italic angle', font.italicangle)

    log_lib.info('writing font parameters')
    json_font_parameters_to_font(font_json['par'])

    log_lib.info('writing font glyphs')
    json_to_glyphs(font_json['glyphs'])

    # gly is a glyph identifier
    # collect all of them:
    glyphs_names_json = [gly for gly in font_json['glyphs']]

    gly_dic = dict([(g.glyphname, g) for g in font.glyphs()])

    glyphs_names_gly_dic = [gly for gly in gly_dic]

    # ordered list of fontforge glyphs:

    for gn in font_json['glyph_list']:
        if gn not in gly_dic:
            log_lib.debug('glyph %s not found in gly_dic' % gn)

    gly_lst = [gly_dic[n] for n in font_json['glyph_list'] if n in gly_dic]

    gly_lst_names = [g.glyphname for g in gly_lst]

    # compare lists of glyph names (for debugging purposes):

    def compare_sets(name_a, a, name_b, b):
        '''
        compare sets of glyph names
        and report the difference to the debug log,
        if the result is nonempty
        '''
        diff = set(a) - set(b)
        if len(diff) > 0:
            message = '[%s] minus [%s] = %s' % (name_a, name_b, str(list(diff)))
            log_lib.debug(message)
            
    compare_sets('glyphs_names_json', glyphs_names_json,
        'glyphs_names_gly_dic', glyphs_names_gly_dic)
    compare_sets('glyphs_names_gly_dic', glyphs_names_gly_dic,
        'glyphs_names_json', glyphs_names_json)
    compare_sets('gly_lst_names', gly_lst_names,
        'glyphs_names_gly_dic', glyphs_names_gly_dic)
    compare_sets('glyphs_names_gly_dic', glyphs_names_gly_dic,
        'gly_lst_names', gly_lst_names)

    # it seems they are equal

    log_lib.info('writing font encodings')
    set_encoding(font_json['encodings'])

    # reasonable state (uses indirect access to (items in) global font.glyphs():

    log_lib.info('writing kern data')
    kern_info_to_font(font_json['kerns'])

    # 05.03.2019 17:42:51:
    log_lib.info('writing font features')
    feature_strings_to_font(font_json['features'])

    log_lib.debug('aalt, accor, ahint:', aalt, acorr, ahint)

    # possibly make an AALT feature:
    if aalt:
        log_lib.info("regenerating AALT feature")
        font.buildOrReplaceAALTFeatures()

    # auto correct the direction of paths
    # using FontForge functions:
    if acorr:
        log_lib.info("auto correcting directions of paths")
        for n, g in list(gly_dic.items()):
            g.correctDirection()
            if g.changed:
                log_lib.debug("%-20s paths corrected" % n)
            g.canonicalStart()

    # auto hint the font
    # using the FontForge function autoHint:
    if ahint:
        log_lib.info("auto hinting font")
        for n, g in list(gly_dic.items()):
            g.autoHint()


    goadb = font_json['goadb']

    # rename glyphs based on the information just read:
    # why sometimes renaming is done three times?

    # turn off
    # 21.08.2019 01:39:37:
    # renaming info is generated inside the function rename_glyphs
    # ~ log_lib.info('renaming glyphs')
    rename_glyphs(goadb['alias'], goadb['unic'])

    # 24.02.2019 21:03:38
    # a phase of cleaning stopped here

    if extrapars:
        log_lib.info('setting extra font parameters')
        set_extrapars(extrapars)

    calculate_private_dict()

    if ofename:
        ofename = ofename.strip()
        log_lib.info("FEA > %s" % ofename)
        font.generateFeatureFile(ofename)

    # unconditionally, as of 20.04.2020 23:06:02:
    validate_font()

    # genarating sfd moved from here to -- after generating otf
    # 11.03.2020 16:36:38

    if 1:
        if tname:
            tname = tname.strip()
            if (tname=='*'):
                tname = font.fontname + '_T1' + '.pfb'
            rename_glyphs(goadb['xalias'])
            log_lib.info("Type1 > %s" % tname)
            font.generate(tname, flags=('afm', 'pfm',))
            log_lib.info('renaming Type1 glyphs')
            rename_glyphs(goadb['alias'])
            oti_fnt = font_json['oti_par']
            log_lib.info('fixing AFM file generated by Fontforge (will be replaced, anyway)')
            fix_afm(tname.replace('.pfb', '.afm'), oti_fnt)
            log_lib.info('fixing PFB file generated by Fontforge')
            fix_pfm(tname.replace('.pfb', '.pfm'), oti_fnt)

    if oname:
        # temporarily not removing, untill it is reprogrammed
        # 21.08.2019 01:35:48:
        remove_redundant_glyphs(goadb)
        oname = oname.strip()
        if (oname=='*'):
            oname = font.fontname + '_OT' + '.otf'
        log_lib.info("OTF > %s" % oname)
        font.generate(oname, flags=('opentype',))

    if sname:
        if sname == True:
            sname = iname + '.sfd'
        sname = sname.strip()
        log_lib.info("SFD > %s" % sname)
        font.save(sname)
        # font.saveNamelist(iname + '.nam')
        # AVOID core dump with ligatures (reopen font):
        # font.close()
        # font = fontforge.open(sname)

    font.close()
    
    # finally flush the info in the log files:
    
    log.log_file_flush()
    log.debug_file_flush()


if __name__ == '__main__':
    main()"""
log_lib_str = r"""#!/usr/bin/python3
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

"""
pfm2_str = r"""# This library is a part of the ReportLab PDF Toolkit, https://www.reportlab.com/opensource/
# (C) Copyright ReportLab Europe Ltd. 2000-2017. See LICENSE.txt for license details:
# BSD license, https://bitbucket.org/rptlab/reportlab/src/
#
# Original pfm.py module source is in:
# https://bitbucket.org/rptlab/reportlab/src/1e4e0e4427ab/src/rl_addons/renderPM/

import struct

class _BUILDER:
    '''Virtual base helper class for structured file scanning'''
    def _get_struct_fmt(self,info):
        fmt = '<'
        for f, _, _ in info:
            fmt += f
        return fmt

    def _get_N_fmt(self,N,fmt):
        return len(fmt)==1 and ('<%d%c' % (N,fmt)) or ('<'+N*fmt)
        
    def _attr_names(self,*I):
        A = []
        for i in I:
            if isinstance(i, basestring):
                A.append(i)
            else:
                A.extend([x[1] for x in i])
        return A

    def _scan_from_file(self,f,info):
        fmt = self._get_struct_fmt(info)
        size = struct.calcsize(fmt)
        T = struct.unpack(fmt,f.read(size))
        i = 0
        for _, n, _ in info:
            setattr(self,n,T[i])
            i = i + 1
            
    def _scanZTStr(self,f,loc):
        '''scan a zero terminated string from the file'''
        f.seek(loc)
        s = ''
        while 1:
            c = f.read(1)
            if c=='\000': break
            s = s+c
        return s

    def _scanN(self,N,fmt,f,loc):
        if not loc: return None
        f.seek(loc)
        fmt = self._get_N_fmt(N,fmt)
        size = struct.calcsize(fmt)
        return struct.unpack(fmt,f.read(size))

    def _scanNT(self,T,N,fmt,f,loc):
        if not loc: return None
        n = len(fmt)
        X = []
        i = 0
        S = []
        for x in self._scanN(N,fmt,f,loc):
            S.append(x)
            i = i + 1
            if i==n:
                X.append(S)
                i = 0
                S = []
        return list(map(lambda x,T=T: T(*x),X))

    
    def _dump(self,A):
        for a in A:
            print(a, getattr(self,a))
            
    def _size_Struct(self,info):
        fmt = self._get_struct_fmt(info)
        return struct.calcsize(fmt)

    def _size_N(self,N,fmt):
        if N == 0: return 0
        fmt = self._get_N_fmt(N,fmt)
        return struct.calcsize(fmt)

    def _check_value(self, s, v):
        if hasattr(self, s):
            if getattr(self,s)!=v:
                # print(s, getattr(self, s), v)
                setattr(self,s,v)
        else:
            # print(s, 'None', v)
            setattr(self,s,v)
            
        
    def _write_Struct(self,info):
        fmt = self._get_struct_fmt(info)
        T = []; i = 0
        for _, n, _ in info:
            T.append(getattr(self,n))
            i = i + 1
        return struct.pack(fmt,*T)
            
    def _writeZTStr(self,info):
        '''write a zero terminated string to a string'''
        return info.encode('iso_8859_1')+'\000'

    def _writeN(self,N,fmt,T):
        fmt = self._get_N_fmt(N,fmt)
        return struct.pack(fmt,*T)

    def _writeNT(self,N,fmt,T):
        X = []
        for x in T:
            X.extend(x.write())
        return self._writeN(N,fmt,X)

            
class KernPair:
    '''hold info about a possible kerning pair'''
    def __init__(self,first,second,amount):
        self.first = first
        self.second = second
        self.amount = amount
    '''return tuple representing kern pair'''
    def write(self):
        return (self.first, self.second, self.amount)

class KernTrack:
    def __init__(self,degree,minSize,minAmount,maxSize,maxAmount):
        '''
        degree  amount to change the character spacing. Negative values mean closer together,p
                ositive values mean farther apart.
        minSize minimum font height (in device units) for which to use linear track kerning.
        minAmount track kerning amount to use for font heights less or equal ktMinSize.
        maxSize maximum font height (in device units) for which to use linear track kerning.f
                For font heights between ktMinSize and ktMaxSize the track kerning amount has
                to increase linearily from ktMinAmount to ktMaxAmount.
        maxAmount track kerning amount to use for font heights greater or equal ktMaxSize.
        '''
        self.degree = degree
        self.minSize = minSize
        self.minAmount = minAmount
        self.maxSize = maxSize
        self.maxAmount = maxAmount
        
    '''return tuple representing kern track'''
    def write(self):
        return (self.degree, self.minSize, self.minAmount, self.maxSize, self.maxAmount)
        

class PFM(_BUILDER):
    def __init__(self,fn=None):
        if fn:
            if isinstance(fn, basestring):
                f = open(fn,'rb')
            else:
                f = fn
            self.scan_from_file(f)
            if f is not fn: f.close()

    '''Class to hold information scanned from a type-1 .pfm file'''
    def scan_from_file(self,f):
        self._scan_from_file(f,self._header_struct_info)
        if self.dfType!=0x81: raise ValueError("Not a Type-1 Font description")
        else: self.WidthTable = None
        self._scan_from_file(f,self._extension_struct_info)
        if not self.dfExtentTable: raise ValueError("dfExtentTable is zero")
        if not self.dfExtMetricsOffset: raise ValueError("dfExtMetricsOffset is zero")
        if self.dfDevice: self.DeviceName = self._scanZTStr(f,self.dfDevice)
        else: self.DeviceName = None
        if self.dfFace: self.FaceName = self._scanZTStr(f,self.dfFace)
        else: self.FaceName = None
        f.seek(self.dfExtMetricsOffset)
        self._scan_from_file(f, self._extTextMetrics_struct_info)
        N = self.dfLastChar - self.dfFirstChar + 1
        self.ExtentTable = self._scanN(N,'H',f,self.dfExtentTable)
        if self.dfDriverInfo: self.DriverInfo = self._scanZTStr(f,self.dfDriverInfo)
        else: self.DriverInfo = None
        if self.dfPairKernTable:
            if self.etmKernPairs!=self._scanN(1,'h',f,self.dfPairKernTable)[0]:
                raise ValueError("inconsistency in etmKernPairs value")
            self.KerningPairs = self._scanNT(KernPair,self.etmKernPairs,'BBh',f,self.dfPairKernTable + 2)
        else: self.KerningPairs = []
        if self.dfTrackKernTable: self.KerningTracks = self._scanNT(KernTrack,self.etmKernTracks,'hhhhh',f,self.dfTrackKernTable)
        else: self.KerningTracks = []

    def write_to_string(self):
        self._check_consistency()
        res = self._write_Struct(self._header_struct_info)
        res += self._write_Struct(self._extension_struct_info)
        res += self._write_Struct(self._extTextMetrics_struct_info)
        if self.DeviceName:
            res += self._writeZTStr(self.DeviceName)
        if self.FaceName:
            res += self._writeZTStr(self.FaceName)
        if self.DriverInfo:
            res += self._writeZTStr(self.DriverInfo)
        N = self.dfLastChar - self.dfFirstChar + 1
        res += self._writeN(N, 'H', self.ExtentTable)
        if self.KerningPairs:
            res += self._writeN(1, 'h', (self.etmKernPairs,))
            res += self._writeNT(self.etmKernPairs, 'BBh', self.KerningPairs)
        if self.KerningTracks:
            res += self._writeNT(self.etmKernTracks, 'hhhhh', self.KerningTracks)   
        return res
        
    def write_to_file(self,fn):
        if isinstance(fn, basestring):
            f = open(fn,'wb')
        else:
            f = fn
        f.write(self.write_to_string())
        if f is not fn: f.close()

    def dump(self):
        self._dump(
            self._attr_names(
            self._header_struct_info,'WidthTable',
            self._extension_struct_info,
            'DeviceName',
            'FaceName',
            self._extTextMetrics_struct_info,
            'DriverInfo',
            ))

    def _check_consistency(self):
        if self.dfType!=0x81: raise ValueError("Not a Type-1 Font description")
        if not self.dfExtentTable: raise ValueError("dfExtentTable is zero")
        if not self.dfExtMetricsOffset: raise ValueError("dfExtMetricsOffset is zero")
        # calculate lenghts
        Header_size = self._size_Struct(self._header_struct_info)
        Extension_size = self._size_Struct(self._extension_struct_info)
        Device_size = self.DeviceName and len(self.DeviceName)+1 or 0
        FaceName_size = self.FaceName and len(self.FaceName)+1 or 0
        ExtMetrics_size = self._size_Struct(self._extTextMetrics_struct_info)
        N = self.dfLastChar - self.dfFirstChar + 1
        Extent_size = self._size_N(N,'H')
        DriverInfo_size = self.DriverInfo and len(self.DriverInfo)+1 or 0
        if self.etmKernPairs>0:
            KernPairs_size = self._size_N(1,'h')+self._size_N(self.etmKernPairs,'BBh')
        else:
            KernPairs_size = 0
        KernTrack_size = self._size_N(self.etmKernTracks,'hhhhh')
        PFM_size = Header_size + Extension_size + Device_size + FaceName_size +\
            ExtMetrics_size + Extent_size + DriverInfo_size +\
            KernPairs_size + KernTrack_size
        # check constants
        if Extension_size!=0x001e or ExtMetrics_size!=0x0034:
            raise ValueError("It can't happen")
        self._check_value('dfVersion', 0x0100) # 1.0    
        self._check_value('dfType', 0x0081) # vector Type 1
        self._check_value('dfPoints', 0x000a) # 10 pt
        self._check_value('dfVertRes', 0x012C) # 300 dpi
        self._check_value('dfHorizRes', 0x012C) # 300 dpi
        self._check_value('dfSizeFields', Extension_size) # struct size
        self._check_value('etmSize', ExtMetrics_size) # struct size
        self._check_value('etmMasterHeight', 0x03E8) # 1000
        self._check_value('etmMinScale', 0x0003)
        self._check_value('etmMaxScale', 0x03E8) # 1000
        self._check_value('dfOriginTable', 0)
        self._check_value('dfReserved', 0)
        # and other values
        self._check_value('etmKernPairs', len(self.KerningPairs))
        self._check_value('etmKernTracks', len(self.KerningTracks))
        if len(self.dfCopyright)!=60:
            self.dfCopyright = self.dfCopyright + "\x00" * (60-len(self.dfCopyright))
        # calculate offsets
        self._check_value('dfSize', PFM_size)
        offset = Header_size + Extension_size
        self._check_value('dfExtMetricsOffset', offset)
        offset += ExtMetrics_size
        if self.DeviceName:
            self._check_value('dfDevice', offset)
            offset += Device_size
        if self.FaceName:
            self._check_value('dfFace', offset)
            offset += FaceName_size
        if self.DriverInfo:
            self._check_value('dfDriverInfo', offset)
            offset += DriverInfo_size
        self._check_value('dfExtentTable', offset)
        offset += Extent_size
        if self.KerningPairs:
            self._check_value('dfPairKernTable', offset)
            offset += KernPairs_size
        if self.KerningTracks:
            self._check_value('dfTrackKernTable', offset)
            offset += KernTrack_size
        if offset != self.dfSize:
            raise ValueError("It can't happen")


    _header_struct_info = (('H','dfVersion',
'''This field contains the version of the PFM file.
For PFM files that conform to this description
(namely PFM files for Type-1 fonts) the
value of this field is always 0x0100.'''),

('i','dfSize',
'''This field contains the total size of the PFM file in bytes.
Some drivers check this field and compare its value with the size of the PFM
file, and if these two values don't match the font is ignored
(I know this happens e.g. with Adobe PostScript printer drivers). '''),

('60s','dfCopyright',
'''This field contains a null-terminated copyright
string, often from the application that created the
PFM file (this normally isn't the
copyright string for the font file itself).
The unused bytes in this field should be set to zero. '''),

('H','dfType',
'''This field contains the font type. The low-order
byte is a combination of the following values
(only the values being of interest in PFM
files are given):

0x00 (PF_RASTER_TYPE): font is a raster font
0x01 (PF_VECTOR_TYPE): font is a vector font
0x80 (PF_DEVICE_REALIZED): font realized by the device driver

The high-order byte is never used in PFM files, it is always zero.

In PFM files for Type-1 fonts the value in this field is always 0x0081. '''),

('H','dfPoints',
'''This field contains the point size at which this font
looks best. Since this is not relevant for scalable fonts
the field is ignored. The value
of this field should be set to 0x000a (10 pt). '''),

('H','dfVertRes',
'''This field contains the vertical resolution at which the
font was digitized (the value is in dots per inch).
The value of this field should be
set to 0x012C (300 dpi). '''),

('H','dfHorizRes',
'''This field contains the horizontal resolution at which
the font was digitized (the value is in dots per inch).
The value of this field should
be set to 0x012C (300 dpi). '''),

('H','dfAscent',
'''This field contains the distance from the top of a
character definition cell to the baseline of the
typographical font. It is useful for aligning the
baseline of fonts of different heights. '''),

('H','dfInternalLeading',
'''This field contains the amount of leading inside
the bounds set by the dfPixHeight field in the PFMHEADER
structure. Accent marks may occur in this area. '''),

('H','dfExternalLeading',
'''This field contains the amount of extra leading that the
designer requests the application to add between rows. Since this area is
outside the character definition cells, it contains no marks and will not be altered by text outputs. '''),

('B','dfItalic',
'''This field specifies whether this font is an italic
(or oblique) font. The low-order bit is 1 if the flag
is set, all other bits are zero. '''),

('B','dfUnderline',
'''This field specifies whether this font is an underlined
font. The low-order bit is 1 if the flag is set, all other
bits are zero. '''),

('B','dfStrikeOut',
'''This field specifies whether this font is a striked-out font.
The low-order bit is 1 if the flag is set, all other bits are zero. '''),

('H','dfWeight',
'''This field contains the weight of the characters in this font.
The value is on a scale from 0 through 1000, increments are in
steps of 100 each. The values roughly give the number of black
pixel from every 1000 pixels. Typical values are:

0 (FW_DONTCARE): unknown or no information
300 (FW_LIGHT): light font
400 (FW_NORMAL): normal font
700 (FW_BOLD): bold font '''),

('B','dfCharSet',
'''This field specifies the character set used in this font.
It can be one of the following values (probably other values
may be used here as well):

0x00 (ANSI_CHARSET): the font uses the ANSI character set;
this means that the font implements all characters needed for the
current Windows code page (e.g. 1252). In case of a Type-1 font
this font has been created with the encoding StandardEncoding
Note that the code page number itself is not stored in the PFM file.

0x02 (SYMBOL_CHARSET): the font uses a font-specific encoding
which will be used unchanged in displaying an printing text
using this font. In case of a Type-1 font this font has been
created with a font-specific encoding vector. Typical examples are
the Symbol and the ZapfDingbats fonts.

0xFF (OEM_CHARSET): the font uses the OEM character set; this
means that the font implements all characters needed for the
code page 437 used in e.g. MS-DOS command line mode (at least
in some versions of Windows, others might use code page
850 instead). In case of a Type-1 font this font has been created with a font-specific encoding vector. '''),

('H','dfPixWidth',
'''This field contains the width of all characters in the font.
For raster fonts this field contains the width in pixels of every
character bitmap if the font is fixed-pitch, otherwise this field
is zero and the character's widths are specified in the WidthTable
table. For vector fonts this field contains the width of the grid
on which the font was digitized. The value is ignored by PostScript
printer drivers. '''),

('H','dfPixHeight',
'''This field contains the height of all characters in the font.
For raster fonts this field contains the height in scan lines of
every character bitmap. For vector fonts this field contains the
height of the grid on which the font was digitized. The value is
ignored by PostScript printer drivers. '''),

('B','dfPitchAndFamily',
'''This field specifies the font pitch and the font family. The
font pitch specifies whether all characters in the font have the
same pitch (this is called fixed pitch too) or variable pitch.
The font family indicates, in a rather general way, the look of a font.

The least significant bit in this field contains the pitch flag.
If the bit is set the font is variable pitch, otherwise it's fixed pitch. For
Type-1 fonts this flag is set always, even if the Type-1 font is fixed pitch.

The most significant bits of this field specify the font family.
These bits may have one of the following values:

0x00 (FF_DONTCARE): no information
0x10 (FF_ROMAN): serif font, variable pitch
0x20 (FF_SWISS): sans serif font, variable pitch
0x30 (FF_MODERN): fixed pitch, serif or sans serif font
0x40 (FF_SCRIPT): cursive or handwriting font
0x50 (FF_DECORATIVE): novelty fonts '''),

('H','dfAvgWidth',
'''This field contains the average width of the characters in the font.
For a fixed pitch font this is the same as dfPixWidth in the
PFMHEADER structure. For a variable pitch font this is the width
of the character 'X'. '''),

('H','dfMaxWidth',
'''This field contains the maximum width of the characters in the font.
For a fixed pitch font this value is identical to dfAvgWidth in the
PFMHEADER structure. '''),

('B','dfFirstChar',
'''This field specifies the first character code defined by this font.
Width definitions are stored only for the characters actually present
in a font, so this field must be used when calculating indexes into the
WidthTable or the ExtentTable tables. For text fonts this field is
normally set to 0x20 (character space). '''),

('B','dfLastChar',
'''This field specifies the last character code defined by this font.
Together with the dfFirstChar field in the PFMHEADER structure this
field specifies the valid character range for this font. There must
be an entry in the WidthTable or the ExtentTable tables for every
character between these two values (including these values themselves).
For text fonts this field is normally set to 0xFF (maximum
possible value). '''),

('B','dfDefaultChar',
'''This field specifies the default character to be used whenever a
character is used that is outside the range of the dfFirstChar through
dfLastChar fields in the PFMHEADER structure. The character is given
relative to dfFirstChar so that the actual value of the default
character is the sum of dfFirstChar and dfDefaultChar. Ideally, the
default character should be a visible character in the current font,
e.g. a period ('.'). For text fonts this field is normally set to
either 0x00 (character space) or 0x75 (bullet). '''),

('B','dfBreakChar',
'''This field specifies the word-break character. Applications
use this character to separate words when wrapping or justifying lines of
text. The character is given relative to dfFirstChar in the PFMHEADER
structure so that the actual value of the word-break character
is the sum of dfFirstChar and dfBreakChar. For text fonts this
field is normally set to 0x00 (character space). '''),

('H','dfWidthBytes',
'''This field contains the number of bytes in every row of the
font bitmap. The value is always an even quantity so that rows of the
bitmap start on 16 bit boundaries. This field is not used for vector
fonts, it is therefore zero in e.g. PFM files for Type-1 fonts. '''),

('i','dfDevice',
'''This field contains the offset from the beginning of the PFM file
to the DeviceName character buffer. The DeviceName is always
present in PFM files for Type-1 fonts, this field is therefore never zero.'''),

('i','dfFace',
'''This field contains the offset from the beginning of the PFM file
to the FaceName character buffer. The FaceName is always present
in PFM files for Type-1 fonts, this field is therefore never zero. '''),

('i','dfBitsPointer',
'''This field is not used in PFM files, it must be set to zero. '''),

('i','dfBitsOffset',
'''This field is not used in PFM files, it must be set to zero. '''),
)

#'H','WidthTable[]'
#This section is present in a PFM file only when this PFM file describes a
#variable pitch raster font. Since Type-1 fonts aren't raster fonts this
#section never exists in PFM files for Type-1 fonts.'''
#The WidthTable table consists of (dfLastChar - dfFirstChar + 2) entries of type WORD (dfFirstChar and dfLastChar can be found in the
#PFMHEADER structure). Every entry contains the width of the corresponding character, the last entry in this table is extra, it is set to zero.

    _extension_struct_info=(
('H','dfSizeFields',
'''This field contains the size (in bytes) of the
PFMEXTENSION structure. The value is always 0x001e. '''),

('I','dfExtMetricsOffset',
'''This field contains the offset from the beginning
of the PFM file to the ExtTextMetrics section.
The ExtTextMetrics section is always present in PFM
files for Type-1 fonts, this field is therefore never
zero. '''),

('I','dfExtentTable',
'''This field contains the offset from the beginning
of the PFM file to the ExtentTable table. This table
is always present in PFM files for Type-1 fonts, this
field is therefore never zero. '''),

('I','dfOriginTable',
'''This field contains the offset from the beginning
of the PFM file to a table containing origin coordinates
for screen fonts. This table is not present in PFM files
for Type-1 fonts, the field must therefore be set to zero. '''),

('I','dfPairKernTable',
'''This field contains the offset from the beginning of
the PFM file to the KerningPairs table. The value must
be zero if the PFM file doesn't contain a KerningPairs
table. '''),

('I','dfTrackKernTable',
'''This field contains the offset from the beginning of
the PFM file to the KerningTracks table. The value must
be zero if the PFM file doesn't contain a kerningTracks
table. '''),
('I','dfDriverInfo',
'''This field contains the offset from the beginning of
the PFM file to the DriverInfo section. This section is
always present in PFM files for Type-1 fonts, this field
is therefore never zero. '''),

('I','dfReserved',
'''This field must be set to zero. '''),
)

#char DeviceName[]
#The DeviceName character buffer is a null-terminated string
#containing the name of the printer driver family. PFM files
#for Type-1 fonts have the string 'PostScript', PFM files for
#PCL fonts have the string 'PCL/HP LaserJet'.
#char FaceName[]
#The FaceName character buffer is a null-terminated string
#containing the name of the font face. In PFM files for Type-1
#fonts this is normally
#the PostScript name of the font without suffixes like
#'-Bold', '-Italic' etc.
    _extTextMetrics_struct_info = (('h','etmSize',
'''This field contains the size (in bytes) of the
EXTTEXTMETRIC structure. The value is always 0x0034. '''),

('h','etmPointSize',
'''This field contains the nominal point size of the font
in twips (this is a twentieth of a point or 1/1440 inch).
This is the intended graphics art size of the font, the
actual size may differ slightly depending on the resolution
of the output device. In PFM files for Type-1 fonts this value
should be set to 0x00f0 (240 twips or 12 pt). '''),

('h','etmOrientation',
'''This field contains the orientation of the font.
This value refers to the ability of the font to be
imaged on a page of a given orientation. It
can be one of the following values:

0x0000: any orientation
0x0001: portrait (page width is smaller that its height)
0x0002: landscape (page width is greater than its height)

In PFM files for Type-1 fonts this field is always 0x0000
since a Type-1 font can be arbitrarily rotated. '''),

('h','etmMasterHeight',
'''This field contains the font size in device units for
which the values in the ExtentTable table are exact. Since
Type-1 fonts are by convention defined in a box of 1000 x 1000
units, PFM files for Type-1 fonts have the value 0x03E8 (1000,
the number of units per em) in this field. '''),

('h','etmMinScale',
'''This field contains the minimum valid size for the font in
device units. The minimum valid point size can then be calculated
as follows:
(etmMinScale * points-per-inch) / dfVertRes
The value for 'points-per-inch' is normally 72, the dfVertRes
field can be found in the PFMHEADER structure, it contains the
vertical resolution at which the font was digitized (this
value is in dots per inch).

In PFM files for Type-1 fonts the value should be set to 0x0003. '''),

('h','etmMaxScale',
'''This field contains the maximum valid size for the font in
device units. The maximum valid point size can then be calculated
as follows:
(etmMaxScale * points-per-inch) / dfVertRes
(see also above etmMinScale).

In PFM files for Type-1 fonts the value should be set to 0x03E8 (1000). '''),

('h','etmMasterUnits',
'''This field contains the integer number of units per em
where an em equals etmMasterHeight in the EXTTEXTMETRIC structure.
In other words, the etmMasterHeight value is expressed in font
units rather than device units.

In PFM files for Type-1 fonts the value should be set to
0x03E8 (1000). '''),

('h','etmCapHeight',
'''This field contains the height for uppercase characters
in the font (the value is in font units). Typically, the
character 'H' is used for measurement purposes.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmXHeight',
'''This field contains the height for lowercase characters
in the font (the value is in font units). Typically, the
character 'x' is used for measurement purposes.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmLowerCaseAscent',
'''This field contains the distance (in font units) that
the ascender of lowercase letters extends above the baseline.
This distance is typically specified for a lowercase character 'd'.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmLowerCaseDescent',
'''This field contains the distance (in font units) that
the descender of lowercase letters extends below the baseline.
This distance is typically specified for a lowercase character 'p'.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmSlant',
'''This field contains the angle in tenth of degrees clockwise
from the upright version of the font. The value is typically not zero only for
an italic or oblique font.

For Type-1 fonts you may find this value in the AFM file
(search for the entry 'ItalicAngle' and multiply it by 10). '''),

('h','etmSuperScript',
'''This field contains the recommended amount (in font units)
to offset superscript characters from the baseline. This amount
is typically specified by a negative offset. '''),

('h','etmSubScript',
'''This field contains the recommended amount (in font units)
to offset subscript characters from the baseline. This amount
is typically specified by a positive offset. '''),

('h','etmSuperScriptSize',
'''This field contains the recommended size (in font units)
for superscript characters in the font. '''),

('h','etmSubScriptSize',
'''This field contains the recommended size (in font units)
for subscript characters in the font. '''),

('h','etmUnderlineOffset',
'''This field contains the offset (in font units) downward
from the baseline where the top of a single underline bar
should appear.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmUnderlineWidth',
'''This field contains the thickness (in font units) of the underline bar.
For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmDoubleUpperUnderlineOffset',
'''This field contains the offset (in font units) downward from
the baseline where the top of the upper, double underline bar should
appear. '''),

('h','etmDoubleLowerUnderlineOffset',
'''This field contains the offset (in font units) downward
from the baseline where the top of the lower, double underline
bar should appear. '''),

('h','etmDoubleUpperUnderlineWidth',
'''This field contains the thickness (in font units) of the
upper, double underline bar. '''),

('h','etmDoubleLowerUnderlineWidth',
'''This field contains the thickness (in font units) of the
lower, double underline bar. '''),

('h','etmStrikeOutOffset',
'''This field contains the offset (in font units) upward from
the baseline where the top of a strikeout bar should appear. '''),

('h','etmStrikeOutWidth',
'''This field contains the thickness (in font units) of the
strikeout bar. '''),

('H','etmKernPairs',
'''This field contains the number of kerning pairs defined
in the KerningPairs table in this PFM file. The number (and
therefore the table) may not be greater than 512. If the PFM
file doesn't contain a KerningPairs table the value is zero. '''),

('H','etmKernTracks',
'''This field contains the number of kerning tracks defined in
the KerningTracks table in this PFM file. The number (and therefore the
table) may not be greater than 16. If the PFM file doesn't contain
a KerningTracks table the value is zero. '''),
)

#'H','ExtentTable[]'
#The ExtentTable table must be present in a PFM file for a Type-1 font,
#it contains the unscaled widths (in 1/1000's of an em) of the characters
#in the font. The table consists of (dfLastChar - dfFirstChar + 1) entries
#of type WORD (dfFirstChar and dfLastChar can be found in the PFMHEADER
#structure).  For Type-1 fonts these widths can be found in the AFM file.

#DRIVERINFO DriverInfo
#The DriverInfo section must be present in a PFM file for a Type-1 font,
#in this case it consists of a null-terminated string containing the
#PostScript name of the font.

#PAIRKERN KerningPairs[]
# NOT DOCUMENTED: KerningPairs table is preceded by number of kerning pairs = etmKernPairs
#The KerningPairs table need not be present in a PFM file for a Type-1
#font, if it exists it contains etmKernPairs (from the EXTTEXTMETRIC
#structure) entries. Each of these entries looks as follows:
#B kpFirst This field contains the first (left) character of the kerning pair.
#B kpSecond This field contains the second (right) character of the kerning pair.
#h kpKernAmount This field contains the kerning amount in font units, the value
#  is mostly negative.

#KERNTRACK KerningTracks[]
#The KerningTracks table need not be present in a PFM file for a Type-1 font, if it exists it contains etmKernTracks (from the EXTTEXTMETRIC structure) entries. Each of these entries looks as follows:
#h ktDegree This field contains the amount to change the character spacing. Negative values mean closer together, positive values mean farther apart.
#h ktMinSize This field contains the minimum font height (in device units) for which to use linear track kerning.
#h ktMinAmount This field contains the track kerning amount to use for font heights less or equal ktMinSize.
#h ktMaxSize This field contains the maximum font height (in device units) for which to use linear track kerning. For font heights between ktMinSize and ktMaxSize the track kerning amount has to increase linearily from ktMinAmount to ktMaxAmount.
#h ktMaxAmount This field contains the track kerning amount to use for font heights greater or equal ktMaxSize.

if __name__=='__main__':
    from glob import glob
    for f in glob('/Program Files/Adobe/Acrobat 4.0/resource/font/pfm/*.pfm'):
        print(f)
        p=PFM(f)
        p.dump()
"""
pfm3_str = r"""# -*- coding: utf-8 -*-

# This library is a part of the ReportLab PDF Toolkit, https://www.reportlab.com/opensource/
# (C) Copyright ReportLab Europe Ltd. 2000-2017. See LICENSE.txt for license details:
# BSD license, https://bitbucket.org/rptlab/reportlab/src/
#
# Original pfm.py module source taken from:
# https://bitbucket.org/rptlab/reportlab/src/1e4e0e4427ab/src/rl_addons/renderPM/

# adapted to Python 3: March 23, 2020, by Marek Ryćko

import struct
import sys

if sys.version_info.major != 3 or sys.version_info.minor < 7:
    print('This version of pfm module can work with Python at least 3.7')
    print(f"found {sys.version}")
    sys.exit()
    
# We are in Python >= 3.7

def debug(*sl):
    s = ' '.join([str(s) for s in sl])
    # print(s)

class _BUILDER:
    '''Virtual base helper class for structured file scanning'''
    
    def _get_struct_fmt(self, info):
        # Python 3: format is a regular string (not bytes):
        fmt = '<'
        for f, _, _ in info:
            # explicite bytes for Python 3:
            fmt += f
        return fmt

    def _get_N_fmt(self, N, fmt):
        # ~ return len(fmt)==1 and ('<%d%c' % (N,fmt)) or ('<'+N*fmt)
        # Python 3, regular strings:
        # ~ return len(fmt) == 1 and ('<%d%c' % (N, fmt)) or ('<' + N * fmt)
        # more readable:
        
        if len(fmt) == 1:
            # ~ res = '<%d%c' % (N, fmt)
            # fmt is a single character; use %s instead of %c
            debug(fmt, type(fmt))
            res = '<%d%s' % (N, str(fmt))
        else:
            res = '<' + N * str(fmt)
        return res
        
    def _attr_names(self, *I):
        A = []
        for i in I:
            if isinstance(i, str):
                A.append(i)
            else:
                A.extend([x[1] for x in i])
        return A

    def _scan_from_file(self, f, info):
        '''
        scan structured info from a binary file
        '''
        debug(f"scanning pfm substructure from a file {f}")
        fmt = self._get_struct_fmt(info)
        debug(f"substructure format: {fmt}")
        size = struct.calcsize(fmt)
        debug(f"size of substructure {size}")
        T = struct.unpack(fmt, f.read(size))
        i = 0
        for _, n, _ in info:
            debug(f"setting attribute {n}: {T[i]}; {type(T[i])}")
            setattr(self, n, T[i])
            i = i + 1
            
    def _scanZTStr(self,f,loc):
        '''scan a zero terminated string from the file
        Python 3:
        scan a zero terminated bytes string from the file
        returning the bytes value (without the trailing zero byte)
        '''
        f.seek(loc)
        # Python 3: bytes literal to start collecting the final value:
        s = b''
        while 1:
            c = f.read(1)
            # Python 3: bytes literal instead of string literal
            if c == b'\000': break
            s = s + c
        return s

    def _scanN(self, N, fmt, f, loc):
        if not loc: return None
        f.seek(loc)
        debug(f"getting N_fmt {N}, {fmt}")
        fmt = self._get_N_fmt(N, fmt)
        debug(fmt, type(fmt))
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, f.read(size))

    def _scanNT(self,T,N,fmt,f,loc):
        if not loc: return None
        n = len(fmt)
        X = []
        i = 0
        S = []
        for x in self._scanN(N, fmt, f, loc):
            S.append(x)
            i = i + 1
            if i==n:
                X.append(S)
                i = 0
                S = []
        return list(map(lambda x,T=T: T(*x),X))

    
    def _dump(self, A):
        # A is a list of strings, being names of attributes of self
        # hopefully elements of A are not of type bytes
        for a in A:
            print((a, getattr(self, a)))
            
    def _size_Struct(self, info):
        fmt = self._get_struct_fmt(info)
        return struct.calcsize(fmt)

    def _size_N(self, N, fmt):
        if N == 0: return 0
        fmt = self._get_N_fmt(N, fmt)
        return struct.calcsize(fmt)

    def _check_value(self, s, v):
        # s is of type string; its an attribute name
        if hasattr(self, s):
            if getattr(self, s) != v:
                # print(s, getattr(self, s), v)
                setattr(self, s, v)
        else:
            # print(s, 'None', v)
            setattr(self, s, v)
        
    def _write_Struct(self, info):
        fmt = self._get_struct_fmt(info)
        T = []; i = 0
        for _, n, _ in info:
            T.append(getattr(self, n))
            i = i + 1
        return struct.pack(fmt, *T)
            
    def _writeZTStr(self, info):
        '''
        write a zero terminated string to a string
        Python 3:
        encode a string info as a binary string in 'iso_8859_1'
        terminate it with a zero byte and return as a byte string
        '''
        # prepare zero terminated bytes string, zt_bytes:
        debug(f"info bytes: {info}")
        # the original code, encoding character string using some
        # encoder, was just a trick; there is no need to do so
        # zt_bytes = str(info).encode('iso_8859_1') + b'\000'
        zt_bytes = info + b'\000'
        return zt_bytes

    def _writeN(self, N, fmt, T):
        fmt = self._get_N_fmt(N, fmt)
        return struct.pack(fmt, *T)

    def _writeNT(self, N, fmt, T):
        X = []
        for x in T:
            X.extend(x.write())
        return self._writeN(N, fmt, X)

            
class KernPair:
    '''hold info about a possible kerning pair'''
    def __init__(self, first, second, amount):
        self.first = first
        self.second = second
        self.amount = amount
    '''return tuple representing kern pair'''
    def write(self):
        return (self.first, self.second, self.amount)

class KernTrack:
    def __init__(self, degree, minSize, minAmount, maxSize, maxAmount):
        '''
        degree  amount to change the character spacing. Negative values mean closer together,p
                ositive values mean farther apart.
        minSize minimum font height (in device units) for which to use linear track kerning.
        minAmount track kerning amount to use for font heights less or equal ktMinSize.
        maxSize maximum font height (in device units) for which to use linear track kerning.f
                For font heights between ktMinSize and ktMaxSize the track kerning amount has
                to increase linearily from ktMinAmount to ktMaxAmount.
        maxAmount track kerning amount to use for font heights greater or equal ktMaxSize.
        '''
        self.degree = degree
        self.minSize = minSize
        self.minAmount = minAmount
        self.maxSize = maxSize
        self.maxAmount = maxAmount
        
    '''return tuple representing kern track'''
    def write(self):
        return (self.degree, self.minSize, self.minAmount, self.maxSize, self.maxAmount)
        

class PFM(_BUILDER):
    '''
    Class to hold information scanned from a type-1 .pfm file
    '''

    def __init__(self, fn=None):
        # fn is either a filename (file path) or a file handle
        if fn:
            if isinstance(fn, str):
                f = open(fn,'rb')
            else:
                f = fn
            # read info from a binary file
            # and store it in the self structures:
            self.scan_from_file(f)
            # if we opened the file here, we close it also
            # (if the file was already open, we do not bother to close it)
            if f is not fn: f.close()

    def scan_from_file(self, f):
        '''
        read info from a binary file f
        and store it in the self structures
        '''
        # read bytes from a file f and put into the self structures:
        debug("start scanning header_struct_info")
        self._scan_from_file(f, self._header_struct_info)
        
        # untangling this complicated tangle of commands:
        
        if self.dfType != 0x81:
            raise ValueError("Not a Type-1 Font description")
        else:
            self.WidthTable = None
            
        debug("start scanning extension_struct_info")
        self._scan_from_file(f,self._extension_struct_info)
        
        if not self.dfExtentTable:
            raise ValueError("dfExtentTable is zero")

        if not self.dfExtMetricsOffset:
            raise ValueError("dfExtMetricsOffset is zero")

        if self.dfDevice:
            self.DeviceName = self._scanZTStr(f,self.dfDevice)
        else:
            self.DeviceName = None
            
        if self.dfFace:
            self.FaceName = self._scanZTStr(f,self.dfFace)
        else:
            self.FaceName = None
            
        f.seek(self.dfExtMetricsOffset)
        debug("start scanning extTextMetrics_struct_info")
        self._scan_from_file(f, self._extTextMetrics_struct_info)
        debug("end scanning extTextMetrics_struct_info")
        
        N = self.dfLastChar - self.dfFirstChar + 1
        self.ExtentTable = self._scanN(N, 'H', f,self.dfExtentTable)
        
        if self.dfDriverInfo:
            self.DriverInfo = self._scanZTStr(f,self.dfDriverInfo)
        else:
            self.DriverInfo = None
            
        if self.dfPairKernTable:
            if self.etmKernPairs != self._scanN(1, 'h', f, self.dfPairKernTable)[0]:
                raise ValueError("inconsistency in etmKernPairs value")
            self.KerningPairs = self._scanNT(KernPair, self.etmKernPairs, \
                'BBh', f, self.dfPairKernTable + 2)
        else:
            self.KerningPairs = []
            
        if self.dfTrackKernTable:
            self.KerningTracks = self._scanNT(KernTrack, self.etmKernTracks, \
                'hhhhh', f, self.dfTrackKernTable)
        else:
            self.KerningTracks = []

    def write_to_string(self):
        '''
        Generate and return pfm as a binary string.
        '''
        self._check_consistency()
        res = self._write_Struct(self._header_struct_info)
        res += self._write_Struct(self._extension_struct_info)
        res += self._write_Struct(self._extTextMetrics_struct_info)
        if self.DeviceName:
            res += self._writeZTStr(self.DeviceName)
        if self.FaceName:
            res += self._writeZTStr(self.FaceName)
        if self.DriverInfo:
            res += self._writeZTStr(self.DriverInfo)
        N = self.dfLastChar - self.dfFirstChar + 1
        res += self._writeN(N, 'H', self.ExtentTable)
        if self.KerningPairs:
            res += self._writeN(1, 'h', (self.etmKernPairs,))
            res += self._writeNT(self.etmKernPairs, 'BBh', self.KerningPairs)
        if self.KerningTracks:
            res += self._writeNT(self.etmKernTracks, 'hhhhh', self.KerningTracks)   
        return res
        
    def write_to_file(self, fn):
        if isinstance(fn, str):
            f = open(fn, 'wb')
        else:
            f = fn
        # write to a binary string:
        binary_string = self.write_to_string()
        f.write(binary_string)
        if f is not fn:
            f.close()

    def dump(self):
        self._dump(
            self._attr_names(
                self._header_struct_info,
                'WidthTable',
                self._extension_struct_info,
                'DeviceName',
                'FaceName',
                self._extTextMetrics_struct_info,
                'DriverInfo',
            ))

    def _check_consistency(self):
        
        if self.dfType!=0x81:
            raise ValueError("Not a Type-1 Font description")
            
        if not self.dfExtentTable:
            raise ValueError("dfExtentTable is zero")
            
        if not self.dfExtMetricsOffset:
            raise ValueError("dfExtMetricsOffset is zero")
            
        # calculate lenghts
        Header_size = self._size_Struct(self._header_struct_info)
        Extension_size = self._size_Struct(self._extension_struct_info)
        Device_size = self.DeviceName and len(self.DeviceName)+1 or 0
        FaceName_size = self.FaceName and len(self.FaceName)+1 or 0
        ExtMetrics_size = self._size_Struct(self._extTextMetrics_struct_info)
        N = self.dfLastChar - self.dfFirstChar + 1
        Extent_size = self._size_N(N, 'H')
        # tricks:
        DriverInfo_size = self.DriverInfo and len(self.DriverInfo) + 1 or 0
        
        if self.etmKernPairs > 0:
            KernPairs_size = self._size_N(1, 'h') + \
                self._size_N(self.etmKernPairs, 'BBh')
        else:
            KernPairs_size = 0
            
        KernTrack_size = self._size_N(self.etmKernTracks, 'hhhhh')
        PFM_size = Header_size + Extension_size + Device_size + FaceName_size + \
            ExtMetrics_size + Extent_size + DriverInfo_size + \
            KernPairs_size + KernTrack_size
            
        # check constants
        if Extension_size != 0x001e or ExtMetrics_size != 0x0034:
            raise ValueError("It can't happen")
            
        self._check_value('dfVersion', 0x0100) # 1.0    
        self._check_value('dfType', 0x0081) # vector Type 1
        self._check_value('dfPoints', 0x000a) # 10 pt
        self._check_value('dfVertRes', 0x012C) # 300 dpi
        self._check_value('dfHorizRes', 0x012C) # 300 dpi
        self._check_value('dfSizeFields', Extension_size) # struct size
        self._check_value('etmSize', ExtMetrics_size) # struct size
        self._check_value('etmMasterHeight', 0x03E8) # 1000
        self._check_value('etmMinScale', 0x0003)
        self._check_value('etmMaxScale', 0x03E8) # 1000
        self._check_value('dfOriginTable', 0)
        self._check_value('dfReserved', 0)
        # and other values
        self._check_value('etmKernPairs', len(self.KerningPairs))
        self._check_value('etmKernTracks', len(self.KerningTracks))
        
        if len(self.dfCopyright) != 60:
            self.dfCopyright = self.dfCopyright + b"\x00" * \
                (60 - len(self.dfCopyright))
                
        # calculate offsets
        self._check_value('dfSize', PFM_size)
        offset = Header_size + Extension_size
        self._check_value('dfExtMetricsOffset', offset)
        offset += ExtMetrics_size
        if self.DeviceName:
            self._check_value('dfDevice', offset)
            offset += Device_size
        if self.FaceName:
            self._check_value('dfFace', offset)
            offset += FaceName_size
        if self.DriverInfo:
            self._check_value('dfDriverInfo', offset)
            offset += DriverInfo_size
        self._check_value('dfExtentTable', offset)
        offset += Extent_size
        if self.KerningPairs:
            self._check_value('dfPairKernTable', offset)
            offset += KernPairs_size
        if self.KerningTracks:
            self._check_value('dfTrackKernTable', offset)
            offset += KernTrack_size
        if offset != self.dfSize:
            raise ValueError("It can't happen")


    _header_struct_info = (('H','dfVersion',
'''This field contains the version of the PFM file.
For PFM files that conform to this description
(namely PFM files for Type-1 fonts) the
value of this field is always 0x0100.'''),

('i','dfSize',
'''This field contains the total size of the PFM file in bytes.
Some drivers check this field and compare its value with the size of the PFM
file, and if these two values don't match the font is ignored
(I know this happens e.g. with Adobe PostScript printer drivers). '''),

('60s','dfCopyright',
'''This field contains a null-terminated copyright
string, often from the application that created the
PFM file (this normally isn't the
copyright string for the font file itself).
The unused bytes in this field should be set to zero. '''),

('H','dfType',
'''This field contains the font type. The low-order
byte is a combination of the following values
(only the values being of interest in PFM
files are given):

0x00 (PF_RASTER_TYPE): font is a raster font
0x01 (PF_VECTOR_TYPE): font is a vector font
0x80 (PF_DEVICE_REALIZED): font realized by the device driver

The high-order byte is never used in PFM files, it is always zero.

In PFM files for Type-1 fonts the value in this field is always 0x0081. '''),

('H','dfPoints',
'''This field contains the point size at which this font
looks best. Since this is not relevant for scalable fonts
the field is ignored. The value
of this field should be set to 0x000a (10 pt). '''),

('H','dfVertRes',
'''This field contains the vertical resolution at which the
font was digitized (the value is in dots per inch).
The value of this field should be
set to 0x012C (300 dpi). '''),

('H','dfHorizRes',
'''This field contains the horizontal resolution at which
the font was digitized (the value is in dots per inch).
The value of this field should
be set to 0x012C (300 dpi). '''),

('H','dfAscent',
'''This field contains the distance from the top of a
character definition cell to the baseline of the
typographical font. It is useful for aligning the
baseline of fonts of different heights. '''),

('H','dfInternalLeading',
'''This field contains the amount of leading inside
the bounds set by the dfPixHeight field in the PFMHEADER
structure. Accent marks may occur in this area. '''),

('H','dfExternalLeading',
'''This field contains the amount of extra leading that the
designer requests the application to add between rows. Since this area is
outside the character definition cells, it contains no marks and will not be altered by text outputs. '''),

('B','dfItalic',
'''This field specifies whether this font is an italic
(or oblique) font. The low-order bit is 1 if the flag
is set, all other bits are zero. '''),

('B','dfUnderline',
'''This field specifies whether this font is an underlined
font. The low-order bit is 1 if the flag is set, all other
bits are zero. '''),

('B','dfStrikeOut',
'''This field specifies whether this font is a striked-out font.
The low-order bit is 1 if the flag is set, all other bits are zero. '''),

('H','dfWeight',
'''This field contains the weight of the characters in this font.
The value is on a scale from 0 through 1000, increments are in
steps of 100 each. The values roughly give the number of black
pixel from every 1000 pixels. Typical values are:

0 (FW_DONTCARE): unknown or no information
300 (FW_LIGHT): light font
400 (FW_NORMAL): normal font
700 (FW_BOLD): bold font '''),

('B','dfCharSet',
'''This field specifies the character set used in this font.
It can be one of the following values (probably other values
may be used here as well):

0x00 (ANSI_CHARSET): the font uses the ANSI character set;
this means that the font implements all characters needed for the
current Windows code page (e.g. 1252). In case of a Type-1 font
this font has been created with the encoding StandardEncoding
Note that the code page number itself is not stored in the PFM file.

0x02 (SYMBOL_CHARSET): the font uses a font-specific encoding
which will be used unchanged in displaying an printing text
using this font. In case of a Type-1 font this font has been
created with a font-specific encoding vector. Typical examples are
the Symbol and the ZapfDingbats fonts.

0xFF (OEM_CHARSET): the font uses the OEM character set; this
means that the font implements all characters needed for the
code page 437 used in e.g. MS-DOS command line mode (at least
in some versions of Windows, others might use code page
850 instead). In case of a Type-1 font this font has been created with a font-specific encoding vector. '''),

('H','dfPixWidth',
'''This field contains the width of all characters in the font.
For raster fonts this field contains the width in pixels of every
character bitmap if the font is fixed-pitch, otherwise this field
is zero and the character's widths are specified in the WidthTable
table. For vector fonts this field contains the width of the grid
on which the font was digitized. The value is ignored by PostScript
printer drivers. '''),

('H','dfPixHeight',
'''This field contains the height of all characters in the font.
For raster fonts this field contains the height in scan lines of
every character bitmap. For vector fonts this field contains the
height of the grid on which the font was digitized. The value is
ignored by PostScript printer drivers. '''),

('B','dfPitchAndFamily',
'''This field specifies the font pitch and the font family. The
font pitch specifies whether all characters in the font have the
same pitch (this is called fixed pitch too) or variable pitch.
The font family indicates, in a rather general way, the look of a font.

The least significant bit in this field contains the pitch flag.
If the bit is set the font is variable pitch, otherwise it's fixed pitch. For
Type-1 fonts this flag is set always, even if the Type-1 font is fixed pitch.

The most significant bits of this field specify the font family.
These bits may have one of the following values:

0x00 (FF_DONTCARE): no information
0x10 (FF_ROMAN): serif font, variable pitch
0x20 (FF_SWISS): sans serif font, variable pitch
0x30 (FF_MODERN): fixed pitch, serif or sans serif font
0x40 (FF_SCRIPT): cursive or handwriting font
0x50 (FF_DECORATIVE): novelty fonts '''),

('H','dfAvgWidth',
'''This field contains the average width of the characters in the font.
For a fixed pitch font this is the same as dfPixWidth in the
PFMHEADER structure. For a variable pitch font this is the width
of the character 'X'. '''),

('H','dfMaxWidth',
'''This field contains the maximum width of the characters in the font.
For a fixed pitch font this value is identical to dfAvgWidth in the
PFMHEADER structure. '''),

('B','dfFirstChar',
'''This field specifies the first character code defined by this font.
Width definitions are stored only for the characters actually present
in a font, so this field must be used when calculating indexes into the
WidthTable or the ExtentTable tables. For text fonts this field is
normally set to 0x20 (character space). '''),

('B','dfLastChar',
'''This field specifies the last character code defined by this font.
Together with the dfFirstChar field in the PFMHEADER structure this
field specifies the valid character range for this font. There must
be an entry in the WidthTable or the ExtentTable tables for every
character between these two values (including these values themselves).
For text fonts this field is normally set to 0xFF (maximum
possible value). '''),

('B','dfDefaultChar',
'''This field specifies the default character to be used whenever a
character is used that is outside the range of the dfFirstChar through
dfLastChar fields in the PFMHEADER structure. The character is given
relative to dfFirstChar so that the actual value of the default
character is the sum of dfFirstChar and dfDefaultChar. Ideally, the
default character should be a visible character in the current font,
e.g. a period ('.'). For text fonts this field is normally set to
either 0x00 (character space) or 0x75 (bullet). '''),

('B','dfBreakChar',
'''This field specifies the word-break character. Applications
use this character to separate words when wrapping or justifying lines of
text. The character is given relative to dfFirstChar in the PFMHEADER
structure so that the actual value of the word-break character
is the sum of dfFirstChar and dfBreakChar. For text fonts this
field is normally set to 0x00 (character space). '''),

('H','dfWidthBytes',
'''This field contains the number of bytes in every row of the
font bitmap. The value is always an even quantity so that rows of the
bitmap start on 16 bit boundaries. This field is not used for vector
fonts, it is therefore zero in e.g. PFM files for Type-1 fonts. '''),

('i','dfDevice',
'''This field contains the offset from the beginning of the PFM file
to the DeviceName character buffer. The DeviceName is always
present in PFM files for Type-1 fonts, this field is therefore never zero.'''),

('i','dfFace',
'''This field contains the offset from the beginning of the PFM file
to the FaceName character buffer. The FaceName is always present
in PFM files for Type-1 fonts, this field is therefore never zero. '''),

('i','dfBitsPointer',
'''This field is not used in PFM files, it must be set to zero. '''),

('i','dfBitsOffset',
'''This field is not used in PFM files, it must be set to zero. '''),
)

#'H','WidthTable[]'
#This section is present in a PFM file only when this PFM file describes a
#variable pitch raster font. Since Type-1 fonts aren't raster fonts this
#section never exists in PFM files for Type-1 fonts.'''
#The WidthTable table consists of (dfLastChar - dfFirstChar + 2) entries of type WORD (dfFirstChar and dfLastChar can be found in the
#PFMHEADER structure). Every entry contains the width of the corresponding character, the last entry in this table is extra, it is set to zero.

    _extension_struct_info=(
('H','dfSizeFields',
'''This field contains the size (in bytes) of the
PFMEXTENSION structure. The value is always 0x001e. '''),

('I','dfExtMetricsOffset',
'''This field contains the offset from the beginning
of the PFM file to the ExtTextMetrics section.
The ExtTextMetrics section is always present in PFM
files for Type-1 fonts, this field is therefore never
zero. '''),

('I','dfExtentTable',
'''This field contains the offset from the beginning
of the PFM file to the ExtentTable table. This table
is always present in PFM files for Type-1 fonts, this
field is therefore never zero. '''),

('I','dfOriginTable',
'''This field contains the offset from the beginning
of the PFM file to a table containing origin coordinates
for screen fonts. This table is not present in PFM files
for Type-1 fonts, the field must therefore be set to zero. '''),

('I','dfPairKernTable',
'''This field contains the offset from the beginning of
the PFM file to the KerningPairs table. The value must
be zero if the PFM file doesn't contain a KerningPairs
table. '''),

('I','dfTrackKernTable',
'''This field contains the offset from the beginning of
the PFM file to the KerningTracks table. The value must
be zero if the PFM file doesn't contain a kerningTracks
table. '''),
('I','dfDriverInfo',
'''This field contains the offset from the beginning of
the PFM file to the DriverInfo section. This section is
always present in PFM files for Type-1 fonts, this field
is therefore never zero. '''),

('I','dfReserved',
'''This field must be set to zero. '''),
)

#char DeviceName[]
#The DeviceName character buffer is a null-terminated string
#containing the name of the printer driver family. PFM files
#for Type-1 fonts have the string 'PostScript', PFM files for
#PCL fonts have the string 'PCL/HP LaserJet'.
#char FaceName[]
#The FaceName character buffer is a null-terminated string
#containing the name of the font face. In PFM files for Type-1
#fonts this is normally
#the PostScript name of the font without suffixes like
#'-Bold', '-Italic' etc.
    _extTextMetrics_struct_info = (('h','etmSize',
'''This field contains the size (in bytes) of the
EXTTEXTMETRIC structure. The value is always 0x0034. '''),

('h','etmPointSize',
'''This field contains the nominal point size of the font
in twips (this is a twentieth of a point or 1/1440 inch).
This is the intended graphics art size of the font, the
actual size may differ slightly depending on the resolution
of the output device. In PFM files for Type-1 fonts this value
should be set to 0x00f0 (240 twips or 12 pt). '''),

('h','etmOrientation',
'''This field contains the orientation of the font.
This value refers to the ability of the font to be
imaged on a page of a given orientation. It
can be one of the following values:

0x0000: any orientation
0x0001: portrait (page width is smaller that its height)
0x0002: landscape (page width is greater than its height)

In PFM files for Type-1 fonts this field is always 0x0000
since a Type-1 font can be arbitrarily rotated. '''),

('h','etmMasterHeight',
'''This field contains the font size in device units for
which the values in the ExtentTable table are exact. Since
Type-1 fonts are by convention defined in a box of 1000 x 1000
units, PFM files for Type-1 fonts have the value 0x03E8 (1000,
the number of units per em) in this field. '''),

('h','etmMinScale',
'''This field contains the minimum valid size for the font in
device units. The minimum valid point size can then be calculated
as follows:
(etmMinScale * points-per-inch) / dfVertRes
The value for 'points-per-inch' is normally 72, the dfVertRes
field can be found in the PFMHEADER structure, it contains the
vertical resolution at which the font was digitized (this
value is in dots per inch).

In PFM files for Type-1 fonts the value should be set to 0x0003. '''),

('h','etmMaxScale',
'''This field contains the maximum valid size for the font in
device units. The maximum valid point size can then be calculated
as follows:
(etmMaxScale * points-per-inch) / dfVertRes
(see also above etmMinScale).

In PFM files for Type-1 fonts the value should be set to 0x03E8 (1000). '''),

('h','etmMasterUnits',
'''This field contains the integer number of units per em
where an em equals etmMasterHeight in the EXTTEXTMETRIC structure.
In other words, the etmMasterHeight value is expressed in font
units rather than device units.

In PFM files for Type-1 fonts the value should be set to
0x03E8 (1000). '''),

('h','etmCapHeight',
'''This field contains the height for uppercase characters
in the font (the value is in font units). Typically, the
character 'H' is used for measurement purposes.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmXHeight',
'''This field contains the height for lowercase characters
in the font (the value is in font units). Typically, the
character 'x' is used for measurement purposes.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmLowerCaseAscent',
'''This field contains the distance (in font units) that
the ascender of lowercase letters extends above the baseline.
This distance is typically specified for a lowercase character 'd'.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmLowerCaseDescent',
'''This field contains the distance (in font units) that
the descender of lowercase letters extends below the baseline.
This distance is typically specified for a lowercase character 'p'.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmSlant',
'''This field contains the angle in tenth of degrees clockwise
from the upright version of the font. The value is typically not zero only for
an italic or oblique font.

For Type-1 fonts you may find this value in the AFM file
(search for the entry 'ItalicAngle' and multiply it by 10). '''),

('h','etmSuperScript',
'''This field contains the recommended amount (in font units)
to offset superscript characters from the baseline. This amount
is typically specified by a negative offset. '''),

('h','etmSubScript',
'''This field contains the recommended amount (in font units)
to offset subscript characters from the baseline. This amount
is typically specified by a positive offset. '''),

('h','etmSuperScriptSize',
'''This field contains the recommended size (in font units)
for superscript characters in the font. '''),

('h','etmSubScriptSize',
'''This field contains the recommended size (in font units)
for subscript characters in the font. '''),

('h','etmUnderlineOffset',
'''This field contains the offset (in font units) downward
from the baseline where the top of a single underline bar
should appear.

For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmUnderlineWidth',
'''This field contains the thickness (in font units) of the underline bar.
For Type-1 fonts you may find this value in the AFM file. '''),

('h','etmDoubleUpperUnderlineOffset',
'''This field contains the offset (in font units) downward from
the baseline where the top of the upper, double underline bar should
appear. '''),

('h','etmDoubleLowerUnderlineOffset',
'''This field contains the offset (in font units) downward
from the baseline where the top of the lower, double underline
bar should appear. '''),

('h','etmDoubleUpperUnderlineWidth',
'''This field contains the thickness (in font units) of the
upper, double underline bar. '''),

('h','etmDoubleLowerUnderlineWidth',
'''This field contains the thickness (in font units) of the
lower, double underline bar. '''),

('h','etmStrikeOutOffset',
'''This field contains the offset (in font units) upward from
the baseline where the top of a strikeout bar should appear. '''),

('h','etmStrikeOutWidth',
'''This field contains the thickness (in font units) of the
strikeout bar. '''),

('H','etmKernPairs',
'''This field contains the number of kerning pairs defined
in the KerningPairs table in this PFM file. The number (and
therefore the table) may not be greater than 512. If the PFM
file doesn't contain a KerningPairs table the value is zero. '''),

('H','etmKernTracks',
'''This field contains the number of kerning tracks defined in
the KerningTracks table in this PFM file. The number (and therefore the
table) may not be greater than 16. If the PFM file doesn't contain
a KerningTracks table the value is zero. '''),
)

#'H','ExtentTable[]'
#The ExtentTable table must be present in a PFM file for a Type-1 font,
#it contains the unscaled widths (in 1/1000's of an em) of the characters
#in the font. The table consists of (dfLastChar - dfFirstChar + 1) entries
#of type WORD (dfFirstChar and dfLastChar can be found in the PFMHEADER
#structure).  For Type-1 fonts these widths can be found in the AFM file.

#DRIVERINFO DriverInfo
#The DriverInfo section must be present in a PFM file for a Type-1 font,
#in this case it consists of a null-terminated string containing the
#PostScript name of the font.

#PAIRKERN KerningPairs[]
# NOT DOCUMENTED: KerningPairs table is preceded by number of kerning pairs = etmKernPairs
#The KerningPairs table need not be present in a PFM file for a Type-1
#font, if it exists it contains etmKernPairs (from the EXTTEXTMETRIC
#structure) entries. Each of these entries looks as follows:
#B kpFirst This field contains the first (left) character of the kerning pair.
#B kpSecond This field contains the second (right) character of the kerning pair.
#h kpKernAmount This field contains the kerning amount in font units, the value
#  is mostly negative.

#KERNTRACK KerningTracks[]
#The KerningTracks table need not be present in a PFM file for a Type-1 font, if it exists it contains etmKernTracks (from the EXTTEXTMETRIC structure) entries. Each of these entries looks as follows:
#h ktDegree This field contains the amount to change the character spacing. Negative values mean closer together, positive values mean farther apart.
#h ktMinSize This field contains the minimum font height (in device units) for which to use linear track kerning.
#h ktMinAmount This field contains the track kerning amount to use for font heights less or equal ktMinSize.
#h ktMaxSize This field contains the maximum font height (in device units) for which to use linear track kerning. For font heights between ktMinSize and ktMaxSize the track kerning amount has to increase linearily from ktMinAmount to ktMaxAmount.
#h ktMaxAmount This field contains the track kerning amount to use for font heights greater or equal ktMaxSize.

if __name__=='__main__':
    from glob import glob
    for f in glob('/Program Files/Adobe/Acrobat 4.0/resource/font/pfm/*.pfm'):
        print(f)
        p=PFM(f)
        p.dump()
"""

# file calling the main module and function from the ff_make_font package

ff_make_font_run_str = r"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Convenience wrapper for running ff_make_font directly from source tree.'''

from ff_make_font.ff_make_font import main

if __name__ == '__main__':
    main()"""

# ------------------------------------------------------------------------------
# config (some constants):
# ------------------------------------------------------------------------------
run_dir = 'ff_make_font_run_dir'
package_dir = 'ff_make_font'


# ------------------------------------------------------------------------------
# creating directory and file structure:
# ------------------------------------------------------------------------------

def write_file(di, fn, s):
    '''
    Write to directory di
    a file named fn
    containing a string s
    '''
    path = os.path.join(di, fn)
    # prepare a string encoded (utf8) to bytes:
    b = s.encode('utf-8')
    try:
        with open(path, 'wb') as fh:
            fh.write(b)
    except:
        log_lib.critical(f"cannot write file directory {path}")

def create_structure(area, major, minor, micro):
    '''
    Create a directory and file structure
    within a given directory area
    (probably within some temporary directory)
    
    For the Python version either 2 or 3
    as described in the major, minor, micro parameters
    '''
    # 1.
    # remove and create the main directory of the structure:
    run_path = os.path.join(area, run_dir)
    # if the main directory of the structure exists, remove it:
    try:
        shutil.rmtree(run_path)
    except:
        # hopefully the directory did not exist anyway
        pass
    if os.path.exists(run_path):
        # not removed correctly
        log_lib.critical(f"cannot remove directory {run_path}")
    # create the main directory of the structure
    try:
        os.makedirs(run_path)
    except:
        # not created correctly
        log_lib.critical(f"cannot create directory {run_path}")
        
    # 2.
    # remove and create the package directory:
    package_path = os.path.join(area, run_dir, package_dir)
    # if the packag directory exists, remove it:
    try:
        shutil.rmtree(package_path)
    except:
        # hopefully the package directory did not exist anyway
        pass
    if os.path.exists(package_path):
        # not removed correctly
        log_lib.critical(f"cannot remove directory {package_path}")
    # create the package directory:
    try:
        os.makedirs(package_path)
    except:
        # not created correctly
        log_lib.critical(f"cannot create directory {package_path}")
        
    # the main directory and subdirectory created succesfully

    # some files are Python-version-dependent:
    if major == 2 and minor >= 7:
        # must be >= 2.6 for log_lib
        python_version = 2
    elif major == 3 and minor >= 7:
        python_version = 3
    else:
        critical_str = f"Python version {major}.{minor}.{micro} not supported for Fontforge"
        log_lib.critical(critical_str)

    # 3. writing components of the package:
    write_file(package_path, '__init__.py', init_str)
    write_file(package_path, 'at_lib.py', at_lib_str)

    # the ff_make_font file is Python-version-dependent:
    if python_version == 2:
        ff_make_font_str = ff_make_font_str2
    elif python_version == 3:
        ff_make_font_str = ff_make_font_str3
    write_file(package_path, 'ff_make_font.py', ff_make_font_str)

    write_file(package_path, 'log_lib.py', log_lib_str)
    
    # the pfm file is Python-version-dependent:
    if python_version == 2:
        pfm_str = pfm2_str
    elif python_version == 3:
        pfm_str = pfm3_str

    debug_str = f"Using supported Python version {major}.{minor}.{micro} for Fontforge"
    log_lib.debug(debug_str)
        
    # we have supported Python 2 or 3 version:
    write_file(package_path, 'pfm.py', pfm_str)
    
    # 4. writing the calling file:
    write_file(run_path, 'ff_make_font_run.py', ff_make_font_run_str)
    
    # the structure is, hopefully, ready
    
def remove_structure(area):
    '''
    Remove the created directory and file structure
    within a given directory area
    as created by create_structure
    (probably within some temporary directory)
    '''
    run_path = os.path.join(area, run_dir)
    # if the main directory of the structure exists, remove it:
    try:
        shutil.rmtree(run_path)
    except:
        # hopefully the directory did not exist anyway
        pass
    if os.path.exists(run_path):
        # not removed correctly
        log_lib.critical(f"cannot remove directory {run_path}")