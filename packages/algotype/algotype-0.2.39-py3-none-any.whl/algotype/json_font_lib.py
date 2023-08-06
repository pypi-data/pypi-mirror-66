#!/usr/bin/python
# -*- coding: utf-8 -*-

# ~ from __future__ import print_function

'''
Generate a json font
from oti, eps, fea, goadb

questions:

02.04.2019 16:10:20
@BJ what is "extrapar"; should it be a part of json_font?



to do:

-- writing json font at a higher level

'''

__author__ = "Marek Ryćko, Piotr Strzelczyk and Bogus/law Jackowski"
__copyright__ = "Copyright (c) 2017, 2019 by GUST e-foundry"
__credits__ = ['Marek Ryćko', "Piotr Strzelczyk", "Bogusław Jackowski", "Piotr Pianowski"]
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = 'Marek Ryćko'
__email__ = "marek@do.com.pl"
__status__ = "Beta"

# python standard library:
import os.path
import sys
# ~ import string
import re
import gc
from argparse import ArgumentParser
# json module for serialization of structures
import json
import copy







# Algotype library:
# ~ import config
# ~ from ffdklib import *
# ffdklib3 is both Python 2 and Python 3 compatible:
# 05.04.2019 19:09:25:
# removed importing the ffdklib3
# 19.08.2019 23:39:57
# ~ from ffdklib3 import *
# calls to ffdklib3 are now explicite:
# 10.10.2019 15:17:15
import algotype.ffdklib3 as ffdklib3

import algotype.parse_eps as pe

# ~ from parse_goadb import full_read_goadb, parse_goadb, transform_goadb, test_goadb
# ~ from parse_goadb import parse_goadb, transform_goadb, test_goadb
from algotype.goadb_lib import parse_goadb, transform_goadb, test_goadb
import algotype.at_lib as lib
# ~ import math_parser

# prints converted to log_lib function calls:
import algotype.log_lib as log_lib

# gc.disable()
# gc.set_debug(gc.DEBUG_LEAK)

piotr = False




# ------------------------------------------------------------------------------
# to further library:
# ------------------------------------------------------------------------------
def write_file(s, fn, mess):
    '''
    create a file of a filename fn
    write a string s to this file in a text mode
    and display a warning message in case of error
    '''
    try:
        # create a file handler:
        fh = file(fn, 'w')
    except IOError:
        log_lib.critical(mess + ': %s' % fn)

    fh.write(s)
    fh.close()


# ------------------------------------------------------------------------------
# CHAPTER I

# collecting data and storing it in a single json font file
# also saving parts of the data in files, like gaodb.json
# ------------------------------------------------------------------------------




# ------------------------------------------------------------------------------
# setting metainformation (global parameters) of the font:
# ------------------------------------------------------------------------------



def font_parameters_to_json(oti_fnt):
    '''Put the font parameters to the font json structure.
    
    Read various parameters of the font
    from the stucture oti_fnt
    (part of a json stucture representing the oti file)
    and put them in a single json structure
    ready to be put into the otf file, Type1 files or other font forms.
    
    The input structure may be empty or incomplete.
    '''
    
    # previous name “oti” for the name of the input structure
    # replaced by ”of” standing for the oti font (the same as oti_fnt)
    # since it is only part of the oti structure:
    # ~ oti = oti_fnt
    of = oti_fnt

    # output structures to be put into the font info structures
    # they will be part of the constructed json_font, meant to be
    # as general as possible, but also for FontForge:
    attr = {}
    nam = {}
    em = None
    
    
    # --------------------------------------------------------------------------
    # preparing data:
    
    # constant for Algotype (as it used to be in Metatype1):
    em = 1000
    
    # constant attributes for FontForge copied from FFattrConst dictionary:
    # (replace it with dict.update())
    # ~ for par, val in list(ffdklib3.FFattrConst.items()):
        # ~ attr[par] = val
    # replaced with update() 29.12.2019 12:33:58:
    attr.update(ffdklib3.FFattrConst)
        
    # attributes of oti font dictionary ’of’
    # translated to the form necessary for FontForge:
    
    for par, inf in list(of.items()):
        if par in ffdklib3.OTItoFFattrI:
            if par == 'DESIGN_SIZE':
                new_inf = inf.split()[0]
            else:
                new_inf = inf
            at = ffdklib3.OTItoFFattrI[par]
            # ~ log_lib.debug('oti_font to json_font attr (%s: %s) --> (%s: %s)' %
                # ~ (par, inf, at, new_inf))
            if isinstance(at, tuple):
                for a in at:
                   attr[a] = float(new_inf)
            else:
                attr[at] = float(new_inf)
        # oti parameters consistent with OTItoFFattrS keys go to attr:
        if par in ffdklib3.OTItoFFattrS:
            attr[ffdklib3.OTItoFFattrS[par]] = inf
            # ~ log_lib.debug('oti_font to json_font attr (%s: %s) --> (%s: %s)' %
                # ~ (par, inf, ffdklib3.OTItoFFattrS[par], inf))
        # oti parameters consistent with OTItoSFNT keys go to nam:
        if par in ffdklib3.OTItoSFNT:
            nam[ffdklib3.OTItoSFNT[par]] = inf
            # ~ log_lib.debug('oti_font to json_font  nam (%s: %s) --> (%s: %s)' %
                # ~ (par, inf, ffdklib3.OTItoSFNT[par], inf))
        
    # VERSION and FULL_NAME oti font keys go to the nam dictionary:
    # check if spaces after ”;” are OK
    if 'VERSION' in of:
        nam['Version'] = "Version %s;PS %s;ffdkm 0.1" % (of['VERSION'], of['VERSION'])
        if 'FULL_NAME' in of:
            nam['UniqueID'] = "%s;UKWN;%s" % (of['VERSION'], of['FULL_NAME'])
        else:
            nam['UniqueID'] = "%s;UKWN" % (of['VERSION'])
        
    if 'GROUP_NAME' in of:
        nam['Preferred Family'] = of['GROUP_NAME']
        # change between Python 2 and Python 3:
        # ~ n = string.find(of['FAMILY_NAME'], of['GROUP_NAME'])
        # changed on 20.08.2019 00:08:57 to:
        if 'FAMILY_NAME' in of and 'STYLE_NAME' in of:
            n = of['FAMILY_NAME'].find(of['GROUP_NAME'])
            
            if n==0 and (len(of['FAMILY_NAME']) > len(of['GROUP_NAME'])):
                s = of['FAMILY_NAME'][len(of['GROUP_NAME']) + 1:] + ' '
            else:
                s = ''
            if of['STYLE_NAME'] == "Regular" and s:
                nam['Preferred Styles'] = s
            else:
                nam['Preferred Styles'] = s + of['STYLE_NAME']
    else:
        if 'FAMILY_NAME' in of and 'STYLE_NAME' in of:
            nam['Preferred Family'] = of['FAMILY_NAME']
            nam['Preferred Styles'] = of['STYLE_NAME']
        
    # SIZE_NAME and other nam attributes:
    if 'SIZE_NAME' in of and 'FAMILY_NAME' in of and 'STYLE_NAME' in of:
        nam['WWS Family'] = of['FAMILY_NAME'] + ' ' + of['SIZE_NAME']
        nam['WWS Subfamily'] =  of['STYLE_NAME']
        nam['Preferred Family'] = of['FAMILY_NAME']
        if of['STYLE_NAME'] == "Regular" and of['SIZE_NAME']:
            nam['Preferred Styles'] = of['SIZE_NAME']
        else:
            nam['Preferred Styles'] = of['STYLE_NAME'] + ' ' + of['SIZE_NAME']
            
    # family name:
    # change between Python 2 and Python 3:
    # ~ attr['familyname']=string.replace(attr['familyname'], ' ', '')
    # changed on 20.08.2019 00:10:55 to:
    # ~ attr['familyname'] = attr['familyname'].replace(' ', '')
    # 10.10.2019 15:26:29:
    if 'familyname' in attr:
        attr['familyname'] = attr['familyname'].replace(' ', '')


    # the names dictionary, with a single entry:
    names = {'English (US)': nam}
    
    
    # prepare the panose structure:
    
    
    
    
    pan = [2, 0, 5, 3, 0, 0, 0, 0, 0, 0]

    if 'FONT_DIMEN' in of:
        
        
        # setting font panose:

        # according to: https://monotype.github.io/panose/pan2.htm  
        # font.os2_panose[0] = 2 -- style: Latin Text (const.)
        # font.os2_panose[1] = 0 -- serif style: (11-Normal Sans, ...)
        # font.os2_panose[2] = 5 -- weight: Book (8-Bold)
        # font.os2_panose[3] = 3 -- proportion: Modern (5-Extended, 6-Condensed, 9-Monospaced)
        # font.os2_panose[4] = 0 -- contrast: (2-None, 4-Low, 6-Medium)
        # font.os2_panose[5] = 0 -- stroke variatons: (2-No Variation, 3-Gradual/Diagonal)
        # font.os2_panose[6] = 0 -- arm style: -- 
        # font.os2_panose[7] = 0 -- letterform: -- 
        # font.os2_panose[8] = 0 -- midline: --
        # font.os2_panose[9] = 0 -- xheight: (3-Standard, 2-Small, 4-Large)
        # so there is no reason to take the list from the fontforge structure:
        # ~ pan = list(font.os2_panose)

        # moving to the unconditional part, before the if,
        # 10.10.2019 15:32:02
        # ~ pan = [2, 0, 5, 3, 0, 0, 0, 0, 0, 0]
        
        
        
        # PSt, why:
        # font.os2_version = 4  # or 5 -- if it has optical scalling range
        fd = {int(i): float(j) for i, j in list(of['FONT_DIMEN'].items())}
        # 04.03.2019 14:14:53:
        # ~ print pan
        pn_weight = fd[8] / fd[15] # exact as in PANOSE documentation
        if pn_weight > 35: 
            pan[2] = 2
        elif pn_weight > 18: 
            pan[2] = 3
        elif pn_weight > 10: 
            pan[2] = 4
        elif pn_weight > 7.5: 
            pan[2] = 5
        elif pn_weight > 5.5: 
            pan[2] = 6
        elif pn_weight > 4.5: 
            pan[2] = 7
        elif pn_weight > 3.5: 
            pan[2] = 8
        elif pn_weight > 2.5: 
            pan[2] = 9
        elif pn_weight > 2.0: 
            pan[2] = 10
        else:
            pan[2] = 11
        pn_contrast = (fd[15] / fd[21] + fd[17] / fd[20]) / 2.0
        if pn_contrast > 0.8: 
            pan[4] = 2
            pan[5] = 2
        elif pn_contrast > 0.5:
            pan[4] = 4
        else:
            pan[4] = 6
        pn_xheight = fd[5] / fd[8]
        if pn_xheight > 0.66: 
            pan[9] = 4
        elif pn_xheight > 0.5: 
            pan[9] = 3
        else:
            pan[9] = 2

    else:
        pan = None
    
    
    # prepare font version and revision:
    
    # set the font revision calculating it from the font version:
    # we want exact (16.16 bits) value for Revision:
    # ~ print 'version', str(font.version)
    if 'VERSION' in of:
        version = of['VERSION']
    else:
        version = 1.0
    revision = round(float(version)*65536)/65536

    # prepare font bold and italic attributes:
    
    bold = False
    italic = False
    
    # write oti font bold attribute to the FontForge font structure:
    if 'PFM_BOLD' in of and 'STYLE_NAME' in of:
        if int(of['PFM_BOLD']) > 0 or of['STYLE_NAME'].find('Bold') > -1:
            bold = True
            # ~ font.os2_weight = 700
            # ~ font.os2_stylemap |= 32 # bold
        
    # write oti font italic attribute to the FontForge font structure:
    # ~ if int(of['PFM_ITALIC']) > 0 or of['STYLE_NAME'].find('Italic') > -1 or font.italicangle < -2:
    # font.italicangle just after initializig fontforge font would be 0.0 anyway,
    # so there is no point of checking it here:
    if 'PFM_ITALIC' in of and 'STYLE_NAME' in of:
        if int(of['PFM_ITALIC']) > 0 or of['STYLE_NAME'].find('Italic') > -1:
            italic = True
            # ~ font.os2_stylemap |= 1 # italic
    
    

    # names, attr, em — ready
    # pan is a list or None
    # revision is set (also version may be used but it is a repetition)
    # bold and italic set
    
    # --------------------------------------------------------------------------
    # prepare a single structure of the font parameters:
    
    par = {
        'names': names,
        'attr': attr,
        'em': em,
        'pan': pan,
        'revision': revision,
        'bold': bold,
        'italic': italic,
    }
    
    return par    

# ------------------------------------------------------------------------------
# glyphs to encoding:
# ------------------------------------------------------------------------------

def glyphs_to_encoding_structure(oti_gly):
    '''
    MR, 24.02.2019 13:48:49
    partially based on PSt’s function set_encoding.
    take an oti_gly structure
    previously read from the oti file
    and prepare an encoding structure
    to be further serialized to a string, written to a file
    and input to fontforge
    '''
    # prepare the encoding list:
    enc = []
    # by default all 256 encoding entries (0 to 255) are .notdef"
    for i in range(256):
        enc.append('.notdef')
    # some encoding entries will be defined, however:
    for gly, inf in list(oti_gly.items()):
        if ('CODE' in inf) and int(inf['CODE']) > -1:
            enc[int(inf['CODE'])] = gly
    # probably the encoding scheme:
    encname = 'FontSpecific'
    # now enc and encname contain all the necessary information
    res = {'enc': enc, 'encname': encname}
    return res


# ------------------------------------------------------------------------------
# including adobe feature files (as strings) to the json font:
# ------------------------------------------------------------------------------

def read_feature_files(fl):
    '''
    read a (possibly empty) list of names of adobe feature files fl
    and store the files in a form of a list of strings
    each string representing a file
    '''
    features = []
    for fn in fl:
        fn = fn.strip()
        # fn should be a single filename
        log_lib.info("FEA < %s" % fn)
        try:
            fh = open(fn, 'r')
            s = fh.read()
            features.append(s)
        except EnvironmentError as IOError:
            log_lib.critical("Couldn't find FEA file: %s" % fn)
    # features is a (possibly empty) list of strings representing feature files
    return features


# ------------------------------------------------------------------------------
# reading the GOADB file; saving to json and further to json font:
# ------------------------------------------------------------------------------

def goadb_to_json(gname, glyph_name_list):
    '''
    read a GOADB file (Glyph order and alias database), under the name fn
    parse it
    and store in a json structure
    if fn is None
    or there is no file fn
    create an empty structure
    
    glyph_name_list is a(n ordered) list of glyph names
    from the original metapost sources
    
    to do:
    remove file actions from the parser
    '''
    if gname is None:
        goadb = {'alias': {}, 'unic': {}, 'xalias': {}}
    else:
        # remove trailing and leading spaces in the filename
        # (if we accept spaces in filename, removing spaces may be problematic)
        gname = gname.strip()
        log_lib.info("GOADB < %s" % gname)
        # parse the GOADB file, using read_goadb from ffdklib
        # taking as parameters the input file name
        # and the current glyph names (keys from gly_dic)
        # (should be less information passed here;
        # passing the full gly_dic is too dangerous)
        # ~ alias, unic, xalias = read_goadb(fn, gly_dic)
        
        # prepare a goadb string:
        
        try:
            # fgoadb = file(gname, 'r')
            # 21.02.2019 03:29:33:
            fh = open(gname, 'r')
            s = fh.read()
            fh.close()
        except IOError:
            log_lib.critial("Couldn't find GOADB file: %s" % gname)
            s = None
        
        # ~ print s[:50]
            
        # ~ alias, unic, xalias = read_goadb(fn, s, glyph_name_list)
        # ~ goadb_old = {'alias': alias, 'unic': unic, 'xalias': xalias}

        if s is not None:
            if 1:
                # new parsing and translation:
                goadb = transform_goadb(parse_goadb(s))
                if goadb['ok']:
                    log_lib.info('GOADB parsing succesful')
                else:
                    log_lib.warning('GOADB parsing with warnings (see the debug file)')
                    wl = goadb['warns']
                    for i, w in enumerate(wl):
                        log_lib.debug(f"GOADB warning[{i}]: {w}")
                    
                # test the glyph list from this font
                # against the goadb
                warns = test_goadb(goadb, glyph_name_list)
                if len(warns) > 0:
                    log_lib.debug('GOADB parse warnings:')
                    for w in warns:
                        log_lib.debug(w)
            else:
                # old (PiotrS) reading:
                pass
                # ~ alias, unic, xalias = full_read_goadb(s, glyph_name_list)
                # ~ goadb = {'alias': alias, 'unic': unic, 'xalias': xalias}
        else:
            # could not read the file 
            goadb = {'alias': {}, 'unic': {}, 'xalias': {}}

    # ~ compare_dictionaries(goadb_old, goadb_new)
    # ~ deep_compare_dictionaries(goadb_old, goadb_new)


    return goadb



    
# ------------------------------------------------------------------------------
# library; converting from strings tu numbers:
# ------------------------------------------------------------------------------
def str_to_number(s):
    '''transform string to int or float
    '''
    n = None
    try:
        n = int(s)
    except ValueError:
        n = float(s)
    except ValueError:
        log_lib.critical('cannot convert string %s to number' % s)
    return n



# ------------------------------------------------------------------------------
# glyph outlines:
# ------------------------------------------------------------------------------
def glyph_json(inf, gly_id, ename):
    '''
    create and return
    a json structure
    containing information about a single glyph
    of an id gly_id
    with structural info inf taken from oti file
    '''
    # codepoint None represents no intention of putting this glyph
    # to a specific codepoint (glyph number)
    codepoint = None
    
    # the CODE field in OTI glyphs dictionary is stored here
    # CODE/code is the intended glyph code in Type1/PFB/AFM default encoding:
    code = inf['CODE']
    
    glyph_name = gly_id

    metrics = {}
    # ~ print inf
    # inf is like:
    # {'WD': '425 HT 734 DP 0 IC 0', 'EPS': '1929', 'CODE': '-1',
    #       'BBX': '86 490 340 734', 'HSBW': '425', 'MATH': 'T'}
    # prepare metric glyph information:
    if 'WD' in inf:
        # take metric information from inf
        # ~ print inf['WD']
        # inf['WD'] is like:
        # 617 HT 709 DP -209 IC 0
        # or like:
        # 440 HT 739 DP 0 IC 19 GA 136.5
        if piotr:
            m = inf['WD'].split()
            metrics['width'] = int(float(m[0]))
            if m[1] == 'HT':
                metrics['textheight'] = int(float(m[2]))
            if m[3] == 'DP':
                metrics['textdepth'] = int(float(m[4]))
        else:
            m = inf['WD'].split()
            metrics['width'] = str_to_number(m[0])
            if m[1] == 'HT':
                metrics['textheight'] = str_to_number(m[2])
            if m[3] == 'DP':
                metrics['textdepth'] = str_to_number(m[4])
    else:
        pass
        # ~ print glyph_name, inf
            
            
    # this function is used both in contexts, when eps files are
    # known and when the files are not (yet) defined
    # ename = None indicates not using eps files
            
    eps = None
    # if ename is None, then there is no eps parsing
    # (changed 03.12.2019 01:20:41 to use partial glyph data)
    if ename is not None and 'EPS' in inf:
        # changed by MR on 22.01.2019 13:48:50:
        # ~ epsname = iname + '.' + inf['EPS']
        # version without renaming someglyph.123 to someglyph.0123.eps
        # ~ epsname = ename + '.' + inf['EPS']
        # 20.02.2019 00:22:26:
        # version with renaming someglyph.123 to someglyph.0123.eps
        epsname = ename + '.' + inf['EPS'].rjust(4, '0') + '.eps'
        # 19.02.2019 23:56:26:
        # ~ print epsname
        
        # put also (practically) empty eps-es to a json structure:
        # used to be:
        # ~ if os.stat(epsname).st_size > 180
        # the length of eps will be checked further
        try:
            fh = open(epsname, 'r')
            # read eps as a string:
            eps = fh.read()
            parsed = pe.parse_eps(eps)
            eps_meta = parsed['meta']
            eps_paths = parsed['body']
        except:
            log_lib.critical("Couldn't read EPS file: %s" % epsname)
            
        # eps info:
        eps_info = {
            # no more storing eps string in the structure
            # as of 10.12.2019 21:58:06:
            # 'eps': eps,
            'meta': eps_meta,
            'paths': eps_paths,
            }
    else:
        log_lib.warning("Missing EPS info in OTI for glyph:\n  %s" % gly)
        eps_info = {
            'eps': '',
            'meta': None,
            'paths': None,
            }
    
    # put all the glyph info to a json structure:
    
    
    
    gj = {
        'codepoint': codepoint,
        'code': code,
        'glyph_name': glyph_name,
        'metrics': metrics,
        # ~ 'eps': eps,
        # ~ 'meta': eps_meta,
        # ~ 'paths': eps_paths,
    }
    
    gj.update(eps_info)

    return gj
    
def glyphs_json(oti, glyn_lst, ename):
    '''
    create a json structure
    containing all the glyphs information
    '''
    glyphs = {}
    for gly in glyn_lst:
        inf = oti[gly]
        gj = glyph_json(inf, gly, ename)
        glyphs[gly] = gj
    return glyphs



# ------------------------------------------------------------------------------
# read kern info from oti and return a structure
# to be used in a json font:
# ------------------------------------------------------------------------------

def kern_info(oti_gly):
    '''
    prepare and return a single kern information for the font
    being a dictionary from glyph names
    to dictionaries of kern values for this particular glyph:
    '''
    kerns = {}
    kern_count = 0
    for gly, inf in list(oti_gly.items()):
        # gly is a glyph name, inf is an oti structure, possibly with kern values
        # ~ print gly, inf
        if 'KPX' in inf:
            # inf['KPX'] is a list of pairs ['glyph_name', '123']
            # where '123' is a string with int kern value
            # ~ print gly, inf['KPX']
            # prepare the kern dictionary for this glyph:
            # ~ log_lib.debug(gly, inf['KPX'])
            kerns[gly] = {}
            for g, val in inf['KPX']:
                kern_count += 1
                try:
                    kerns[gly][g] = int(val)
                except ValueError:
                    kerns[gly][g] = float(val)
                except ValueError:
                    log_lib.warning('cannot convert a value for kern in glyph %s' % gly)
    log_lib.debug('kern count:', kern_count)
    return kerns

# ------------------------------------------------------------------------------
# reading various data and making json font:
# ------------------------------------------------------------------------------

def make_json_font(otiname, fename, gname, ename, joname):
    '''
    read
     -- the oti file, transforming it into structure
     -- (0 or more) feature files from files named in the list fename
     -- a goadb file from the file named gname
     -- eps basename including path
     -- filename for json output oti file/string
    and create a json font — collection of information
    '''

    # create oti structure from oti file:
    
    # read_oti (parser from text to json structures)
    # is in a library, ffdklib (Python3 version: ffdklib3):
    # (replace parser of a file with a parser of a string)
    # ~ oti_fnt, oti_gly, glyn_lst = read_oti(otiname)
    # 20.08.2019 16:35:18:
    oti = ffdklib3.read_oti(otiname)
    # if the oti file was not found, the resulting components
    # of the oti structure are empty

    # oti = {'font': oti_fnt, 'glyphs': oti_gly, 'list': glyn_lst}
    
    # serialization:

    lib.write_json(oti, joname)

    # oti = {'font': oti_fnt, 'glyphs': oti_gly, 'list': glyn_lst}
    oti_fnt = oti['font']
    oti_gly = oti['glyphs']
    glyn_lst = oti['list']

    # gradually preparing a json structure representing
    # all the information of the font:
    font_json = {}
    
    par = font_parameters_to_json(oti_fnt)
    
    # 1. par
    font_json['par'] = par
    
    # 2. oti_par
    # temporarily save also the raw parameters, as taken from oti file:
    font_json['oti_par'] = oti['font']

    # 2a.
    # temporarily save also the raw glyph parameters, as taken from oti file:
    font_json['oti_glyphs'] = oti_gly
    
    gj = glyphs_json(oti_gly, glyn_lst, ename)
    
    # 3.
    # the dictionary of glyphs:
    font_json['glyphs'] = gj
    
    # 4.
    # the list of glyph names:
    font_json['glyph_list'] = glyn_lst
    
    # 5.
    # encodings
    # (already refactored -- MR):
    es = glyphs_to_encoding_structure(oti_gly)
    font_json['encodings'] = es

    # 6.
    # kerns
    ki = kern_info(oti_gly)
    font_json['kerns'] = ki

    # possibly merge (to the font being prepared)
    # feature information from a feature file
    # generated at one of the previous stages of Algotype:

    # 7.
    # read feature files:
    features = read_feature_files(fename)
    font_json['features'] = features
    
    # 8.
    # goadb info:
    
    # from oti we need an ordered list of glyphs:
    # ~ goadb_old, goadb_new = goadb_to_json(gname, glyn_lst)
    
    # glyn_lst comes from oti/metapost
    # and is a list of strings
    # being names of glyphs — source names, before renaming
    goadb = goadb_to_json(gname, glyn_lst)
    font_json['goadb'] = goadb
    # ~ font_json['goadb_new'] = goadb_new

    return font_json

# ------------------------------------------------------------------------------
# json structure transformation
# GOADB renaming and assigning codepoints
# ------------------------------------------------------------------------------
def json_goadb_apply(font_json, goadb):
    '''
    rename glyph names
    and assign codepoints
    in all components of json font
    the definition of renaming and codepoints are in goadb structure
    '''
    def new_glyph_name(old_glyph_name):
        return alias[old_glyph_name] if old_glyph_name in alias else old_glyph_name
    
    old = font_json
    alias = goadb['alias']
    unic = goadb['unic']
    
    # in the log list of strings store the information of actions
    # log of renaming:
    logr = []
    # log of codes:
    logc = []
    # log of renaming in encoding:
    loge = []
    
    # prepare the structure for the new json font
    new = {}
    
    # 1., 2.
    # par and oti_par are not transformed
    new['par'] = old['par']
    new['oti_par'] = old['oti_par']

    # 3.
    # the dictionary of glyphs:

    # prepare the new dictionary of glyphs:
    glyphs = {}
    for k, v in old['glyphs'].items():
        # transform glyph k: v to the new names
        new_glyph = copy.deepcopy(v)
        if k in alias:
            new_glyph['glyph_name'] = alias[k]
            glyphs[alias[k]] = new_glyph
            # if there was a real action, log it:
            if k != alias[k]:
                logr.append('    renaming %30s --> %s' % (k, alias[k]))
            else:
                logr.append('not renaming %30s' % k)
        else:
            # key k not in alias database:
            logr.append('the key %-23s not found in GOADB' % k)
                
        # assign a codepoint to the glyph:
        if k in unic:
            new_glyph['codepoint'] = unic[k]
            # this may be -1 or -10
            
            # ~ if unic[n] != -10:
                # ~ if unic[n] < 0:
                    # ~ log.append("%-20s %04x unicode not in GOADB" % (n, ffunic))
                    
                
            if k in alias:
                logc.append('codepoint %06d %04x %30s --> %s' % (unic[k], unic[k], k, alias[k]))
            else:
                logc.append('codepoint %06d %04x %30s' % (unic[k], unic[k], k))

    new['glyphs'] = glyphs
        
    # 4.
    # the list of glyph names:
    glyph_list = [alias[k] if k in alias else k for k in old['glyph_list']]
    new['glyph_list'] = glyph_list

    # 5.
    # encodings

    # the old['encodings'] entry is of the form:
    # {'enc': enc, 'encname': encname}
    enc_list = old['encodings']['enc']
    new_enc_list = []
    for k in enc_list:
         
        if k in alias:
            ne = alias[k]
            if k != alias[k]:
                loge.append('    renaming %30s --> %s' % (k, alias[k]))
            else:
                loge.append('not renaming %30s' % k)
        else:
            ne = k
            loge.append('not renaming %30s' % k)
        new_enc_list.append(ne)
        
    new['encodings'] = {}
    new['encodings']['enc'] = new_enc_list
    new['encodings']['encname'] = old['encodings']['encname']
    
    # 6.
    # kerns
    new_kerns = {}
    for k, v in old['kerns'].items():
        # kerns for the name k
        # prepare a new entry for this key, replacing v:
        new_table = {}
        for glyph_name, kern in v.items():
            new_table[new_glyph_name(glyph_name)] = kern
        new_kerns[new_glyph_name(k)] = new_table
        
    new['kerns'] = new_kerns
        
    # 7.
    # copy feature files:
    new['features'] = old['features']
        
    # 8.
    # goadb info:
    
    new['goadb'] = old['goadb']
        
        
        
        
        
        
        
    return {'new': new, 'logr': logr, 'logc': logc, 'loge': loge}



# ------------------------------------------------------------------------------
# variables read from a parameter of function call:
# ------------------------------------------------------------------------------

def one_json_font(par):
    
    
    iname = par['iname']
    edir = par['edir'] 
    jgname = par['jgname'] 
    jglname = par['jglname'] 
    joname = par['joname'] 
    jfname = par['jfname'] 

    otiname = par['otiname'] 

    fename = par['fename'] 
    gname = par['gname'] 

    # quiet is not respected yet
    quiet = par['quiet'] 
    pydir = par['pydir'] 
    
    iname  = iname.strip()
    iname = re.sub(r'\.[^\.]+$', '', iname)
    # 22.01.2019 13:46:13:
    bname = os.path.basename(iname)

    # input EPS path (directory and basename) without extension:
    ename = os.path.join(edir, bname)

    if pydir != False:
        sys.path.append(pydir)

    # ------------------------------------------------------------------------------
    # creating json font
    # from oti, eps files, fea file, goadb:

    '''
    read various parameters of the font
    from the stucture oti_fnt
    (part of a json stucture representing the oti file)
    and put them to the json font structure
    '''

    # prepare a json structure representing
    # all the information of the font:

    if not fename:
        fename = []
    # fename is a list of names of feature files

    # gname is to be a name of goadb file:
    if not gname:
        gname = None

    font_json = make_json_font(otiname, fename, gname, ename, joname)

    if 0:
        # run in the new version of transforming names not in fontforge
        res = json_goadb_apply(font_json, font_json['goadb'])
        font_json = res['new']
    
    
    # ~ base = '/1/mini/programowanie/0tematy/fonty/002_nowy_etap_z_poszerzonym_językiem_programowania_konfiguracji/50_out/2019_08_16_17_55/json'
    # ~ with open(os.path.join(base, 'log_renaming.log'), 'w') as fh:
        # ~ fh.write('\n'.join(res['logr']))
        # ~ fh.write('\n%s' % len(res['logr']))
    # ~ with open(os.path.join(base, 'log_codepoint.log'), 'w') as fh:
        # ~ fh.write('\n'.join(res['logc']))
        # ~ fh.write('\n%s' % len(res['logc']))
    # ~ with open(os.path.join(base, 'log_renaming_encoding.log'), 'w') as fh:
        # ~ fh.write('\n'.join(res['loge']))
        # ~ fh.write('\n%s' % len(res['loge']))
        
    # ~ lib.write_json(res['new'], os.path.join(base, 'new_font.json'))

    # parts of the font structure:
    log_lib.info('writing json goadb to %s' % jgname)
    lib.write_json(font_json['goadb'], jgname)
    log_lib.info('writing json glyphs to %s' % jglname)
    lib.write_json(font_json['glyphs'], jglname)

    # serialization:
    log_lib.info('writing json font to %s' % jfname)
    lib.write_json(font_json, jfname)



if __name__ == '__main__':
    # work as a self-contained program
    # ------------------------------------------------------------------------------
    # Start of processing:
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # reading arguments:
    # ------------------------------------------------------------------------------
    # ~ argpars = ArgumentParser(description='METATYPE1 -> Type1 or OpenType converter',
    argpars = ArgumentParser(description='Algotype -> Type1 or OpenType converter',
         fromfile_prefix_chars='@')
    addarg=argpars.add_argument
    # ~ addarg('input', help='Input METATYPE1 filename')
    addarg('input', help='Input Algotype filename')
    # 20.02.2019 00:41:15:
    addarg('-e', '--epsdir', nargs='?', const=False, help='Directory for input EPS files')
    addarg('-p', '--pydir', nargs='?', const=False, help='Directory for Python input files')
    # ~ addarg('-o', '--output', nargs='?', const=False, help='Generated OTF file')
    # ~ addarg('-te', '--tempdir', nargs='?', const=False, help='Temporary directory')
    addarg('-oti', '--oti', nargs='?', const=False, help='Oti file')
    addarg('-jg', '--jsongoadb', nargs='?', const=False, help='Json goadb file')
    addarg('-jgl', '--jsonglyph', nargs='?', const=False, help='Json glyph file')
    addarg('-jo', '--jsonoti', nargs='?', const=False, help='Json oti file')
    addarg('-jf', '--jsonfont', nargs='?', const=False, help='Json font file')
    # ~ addarg('-t', '--typeone', nargs='?', const=False, help='Generated Type1 file')
    # ~ addarg('-s', '--save', nargs='?', const=True, help='Output saved in sfd format')
    addarg('-f', '--fea', nargs='*', help='Feature filename to be used')
    addarg('-g', '--goadb',  nargs='?', const=True, help='GOADB (Glyph order and alias database) to be used')
    # ~ addarg('-a', '--afm', nargs='?', const=True, help='AFM filename to be used')
    # ~ addarg('-m', '--math', nargs='*', help='MATH feature filename to be used')
    # ~ addarg('-x', '--extra',  nargs='*', help='Extra parameters to be set in OTF tables')
    # ~ addarg('-aa', '--aalt', action='store_true', help='Make a AALT feature')
    # ~ addarg('-ah', '--autohint', action='store_true', help='Auto hint all glyphs')
    # ~ addarg('-ac', '--autocorrect', action='store_true', help='Auto correct path (direction and atart points)')
    # ~ addarg('-v', '--validate', nargs='?', const=True, help='Output the report from font validation')
    # ~ addarg('-sf', '--savefea', nargs='?', const=True, help='Output the used features')
    addarg('-q', '--quiet', action='store_true', help='Less messages')


    # ------------------------------------------------------------------------------
    # variables read from command line arguments:


    args = argpars.parse_args()
    iname  = args.input

    # temporarily, 22.01.2019 13:41:10, before making it an argument:
    # input EPS directory:
    # 19.02.2019 23:57:45:
    edir = args.epsdir
    # ~ edir = 'srceps'

    jgname  = args.jsongoadb
    jglname  = args.jsonglyph
    joname  = args.jsonoti
    jfname  = args.jsonfont

    otiname  = args.oti

    fename = args.fea
    gname  = args.goadb

    # quiet is not respected yet
    quiet  = args.quiet


    pydir = args.pydir

    par = {
        'iname': iname,

        # temporarily, 22.01.2019 13:41:10, before making it an argument:
        # input EPS directory:
        # 19.02.2019 23:57:45:
        'edir': edir,
        'jgname': jgname,
        'jglname': jglname,
        'joname': joname,
        'jfname': jfname,

        'otiname': otiname,

        'fename': fename,
        'gname': gname,

        # quiet is not respected yet
        'quiet': quiet,
        'pydir': pydir,

    }


    one_json_font(par)
