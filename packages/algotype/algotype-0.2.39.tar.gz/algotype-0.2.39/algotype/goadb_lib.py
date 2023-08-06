#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
goadb_lib.py

formerly parse_goadb

a set of GOADB services
GOADB = Glyph Order and Alias Data Base
converting glyph names from metapost/eps names
to OTF and to Type1 (PFB) names
and from PFB names to metapost names

including a parser of a GOADB file (string)

Marek Ryćko, based on work by Piotr Strzelczyk

start as a copy of the parsing function
cut out from ffdklib (ffdklib3)
then started as a copy of parse_goadb

goadb_lib is used in:
-- ffdkm, a copy of some code, using alias, xalias, unic
-- in json_font_lib

translated to Python3 at 29.01.2020 11:55:35

'''

# standard library
import re
# for sys.exit:
import sys

# Algotype library:
# (at the moment of 12.01.2020 18:08:34
# goadb_lib is just passing variables from parse_goadb)
# ~ from parse_goadb import *

import algotype.log_lib as log_lib



def parse_goadb(s):
    '''
    parse an input string s
    as a GOADB structure:
    the first level of parsing:
    selecting significant lines and splitting them to fields
    '''
    
    # split the input string to a list of lines:
    # sl -- string list
    sl = s.splitlines()
    # ~ print len(sl)
    
    # filter out empty, whitespace and comment lines:
    pat = '^\s*(\#.*)?$'
    patc = re.compile(pat)
    
    def regular(line):
        '''
        Test if an input line is a regular one (singnificant for parsing).
        '''
        mo = patc.match(line)
        if mo:
            res = False
        else:
            res = True 
        return res
            
    # filter out the irregular lines out of the string list
    sl = list(filter(regular, sl))
    # ~ print len(sl)
    
    # sl is a list of regular lines, hopefully well formed
    
    # remove leading and trailing whitespace:
    
    def strip_line(line):
        new = line.strip()
        # ~ if new != line:
            # ~ print 'whitespace removed', '[%s]' % line, '-->', '[%s]' % new
        return new
        
    sl = list(map(strip_line, sl))
    
    # parse the regular lines and put them into a structure
    # each line will be represented as a list of strings
    
    # collecting data list:
    dl = []
    for line in sl:
        line_structure = re.split(r'[ \t]+', line)
        dl.append(line_structure)
        
    # at this level of parsing all the structures are considered correct
    
    return dl
    
def transform_goadb(data_list):
    '''
    take the data list, being the result of parsing the GOADB file/string
    and transform it to the logical structure reflecting its meaning
    '''
    
    # construct the resulting dictionaries
    # reflecting the logical structure of GOADB info

    # mapping from eps glyph names (source names)
    # to otf glyph names (target names)
    alias = {}
    
    # mapping from otf glyph names (target names)
    # to eps glyph names (source names)
    # only for entries marked as PFBNAME
    xalias = {}
    
    # mapping from eps glyph names (source names)
    # to unicode values
    # and, in some cases, to special values
    unic = {}

    # collect also possible warnings
    # this will be a list of strings
    warns = []
    
    def warn(s):
        warns.append(s)

    for line in data_list:
        # ~ warn(line[1])

        # the almost original line will be useful in warnings:
        almost_original_line = ' '.join(line)
        
        if len(line) < 2 or len(line) > 4:
            # ~ warn('Unrecognized line in GOADB:\n  %s' % ' '.join(line))
            # 31.01.2020 23:20:43:
            # we cannot tolerate malformed GOADB files:
            log_lib.critical(f'Wrong number of fields in GOADB line: {almost_original_line}')
            
        # length is between 2 and 4, inclusive

        # common abbreviations:
        source_name = line[1]
        # target name is the target for OTF font file
        # and also for the Type1 font file, if the names are the same
        # or if the last column reads ‘PFBNAME’
        target_name = line[0]

        # 1.
        # first value in one of the dictionaries:
        # calculating alias dictionary entry:
        if source_name in alias:
            # ~ warn('%s already in alias' % source_name)
            # warning changed to reflect the input syntax/semantics more
            # 31.01.2020 21:53:52:
            log_lib.critical(f'Duplicate glyph name in source names column: {source_name}')
            
        # no repetition of source_name-s yet
        alias[source_name] = target_name

        # 2.
        # calculate unicode entry
        # which in fact may reflect also that
        # the source name is also a pfb name
        
        if len(line) > 2:
            if line[2].upper() == 'PFBNAME':
                un = -1
            elif line[2].upper() == 'SKIP':
                un = -10
            else:
                try:
                    un = int(re.sub(r'u(ni)?', '', line[2]), 16)
                except ValueError:
                    warn("Unrecognized unicode: %s" % line[2])
                    continue
        else:
            # len of line == 2 is equivalent to PFBNAME
            # with respect to calculating the unicode dictionary
            # so line == [A, B] is in this context equivalent to [A, B, 'PFBNAME']
            un = -1
            
        # for all the source names from the second column
        # unicode value for this source name is
        #  -- either an integer number (the unicode codepoint)
        #  -- or -1 for PFBNAME or for unicode index not provided
        #  -- or -10 for skipping, whatever it means

        if source_name in unic:
            warn(f'Duplicate unicode or PFBNAME/SKIP entry for source name {source_name}')
        unic[source_name] = un

        # verify the compatibility between
        # unicode number in the third column (if provided)
        # and unicode number as a part of glyph name in the first column
        # (if the name in the first column has this form,
        # like u12345 or uni2345):
        
        # calculate the matching object mo for the first column:
        mo = re.match(r'^u(ni)?([0-9A-Fa-f]+)$', target_name)
        if mo and un != int(mo.group(2), 16):
            # the string target_name matches the unicode string:
            if un > 0:
                # the string in the third column
                # is the real representation of a unicode point
                # but is different from the unicode from the first column:
                warn(f'OTF name {target_name} not compatible with unicode {un:04x}')
            else:
                # no unicode in the third column:
                warn("OTF name %s, without unicode" % target_name)
                
        # attempt to warn in each non-unicode case:
        if un <= 0:
            # no unicode in the third column:
            warn(f'No unicode specified in line: {almost_original_line}')
            
            
            
        # 3.
        # the xunic dictionary was meant to be the mapping between
        # source (eps) names and unicode values:
        
        # if un in xunic:
        #    warn("Doubled unicode %04x, glyphs %s and %s" % (un, xunic[un], psfn))
        # else:
        #    if un > 0: xunic[un] = psfn
        
        # 4.
        # calculating the xalias entry:
        
        # PSt:
        # ~ if line[len(line) - 1].upper() == 'PFBNAME':
        # MR:
        if line[-1].upper() == 'PFBNAME':
            # if the last field in the line (the third or fourth field)
            # is the 'PFBNAME' string
            
            if target_name in xalias:
                # ~ warn('%s already in unic' % target_name)
                # 31.01.2020 23:53:29:
                # ~ warn(f'Ambigous PFB translation [OTF name:] {target_name} [PFB name:] {source_name}')
                pass
            xalias[target_name] = source_name

    # the three resulting dictionaries
    # and the list of warnings are ready;
    # prepare the resulting json object:
    ok = (len(warns) == 0)
    res = {'alias': alias, 'unic': unic, 'xalias': xalias, 'warns':
        warns, 'ok': ok}
    return res

def goadb_structures(data_list):
    '''
    take the data list, being the result of parsing the GOADB file/string
    and transform it to a group of logical structures reflecting its meaning.
    
    This is planned to be different analysis then in transform_goadb.
    
    
    maybe there will be some functions:
        -- from source names to pfb names
        -- from pfb names to source names
    '''
    # mapping from eps glyph names (source names, oti names)
    # to otf names
    # and, in some cases, to special values
    source_to_otf = {}
    source_to_pfb = {}
    otf_to_source = {}
    pfb_to_source = {}
    # mapping from source names
    # to the structured original lines
    # (mostly for the information/notification purposes)
    source_to_lines = {}



    # collect also possible warnings
    # this will be a list of strings
    warns = []
    
    def warn(s):
        warns.append(s)
        
    for line in data_list:

        # the almost original line will be useful in warnings:
        almost_original_line = ' '.join(line)
        
        if len(line) < 2 or len(line) > 4:
            # ~ warn('Unrecognized line in GOADB:\n  %s' % ' '.join(line))
            # 31.01.2020 23:20:43:
            # we cannot tolerate malformed GOADB files:
            log_lib.critical(f'Wrong number of fields in GOADB line: {almost_original_line}')
            
        # length is between 2 and 4, inclusive
        
        # common abbreviations:
        source_name = line[1]
        # target name is the target for OTF font file
        # and also for the Type1 font file, if the names are the same
        # or if the last column reads ‘PFBNAME’
        target_name = line[0]
        
        # if there is a pfbname tag in the line:
        if_pfbname_tag = (line[-1].lower() == 'pfbname')
        
        # assuming that source names are unique
        # create an entry in the dictionary/mapping
        # from source names to entire structured lines:
        if source_name in source_to_lines:
            # this should not happen; repeated source name:
            log_lib.critical(f'repeated source name {source_name}')
        else:
            source_to_lines[source_name] = line

        # append target name to the list of target names
        if source_name in source_to_otf:
            source_to_otf[source_name].append(target_name)
        else:
            source_to_otf[source_name] = [target_name]

        # append source name to the list of source names
        # for the target_name key:
        if target_name in otf_to_source:
            otf_to_source[target_name].append(source_name)
        else:
            otf_to_source[target_name] = [source_name]

        # create unambigous or ambigous mapping
        # between source names and pfb names
        # first decide what will be the pfb name defined in this line:
        pfb_name = source_name if if_pfbname_tag else target_name
        if source_name in source_to_pfb:
            source_to_pfb[source_name].append(pfb_name)
        else:
            source_to_pfb[source_name] = [pfb_name]

        # append source name to the list of source names
        # for the target_name key:
        if pfb_name in pfb_to_source:
            pfb_to_source[pfb_name].append(source_name)
        else:
            pfb_to_source[pfb_name] = [source_name]
            
            
        was_pfbname = False
        was_skip = False
        for i, v in enumerate(line):
            was_pfbname = was_pfbname or v.lower() == 'pfbname'
            was_skip = was_skip or v.lower() == 'skip'
        both = was_pfbname and was_skip
        if both:
            log_lib.warning('both PFBNAME and SKIP in GOADB lins:', line)

    res = {
        'source_to_otf': source_to_otf,
        'source_to_pfb': source_to_pfb,
        'otf_to_source': otf_to_source,
        'pfb_to_source': pfb_to_source,
        'source_to_lines': source_to_lines,
    }
    return res


    
def augment_goadbY(goadb):
    '''
    Extend GOADB data by a reverse function: from pfb names to oti names.
    
    Take the structural GOADB data
    as was a tradition in Metatype1 (the predecessor of Algotype),
    namely containing the dictionaries:
        -- alias (a function from source names to otf names)
        -- xalias (a function from otf names to pfb names)
        -- unic (a function from otf names to unicodes)
    and augment it with the calculated functions:
        -- from source names to pfb names
        -- from pfb names to source names
    '''
    # mapping from eps glyph names (source names)
    # to unicode values
    # and, in some cases, to special values
    unic = {}

    # collect also possible warnings
    # this will be a list of strings
    warns = []
    
    def warn(s):
        warns.append(s)



    
def test_goadb(goadb, mp_glyph_list):
    '''
    test the set of glyphs names as it comes from metapost/oti
    and the domain/counterdomain of the alias database
    '''

    # collect also possible warnings
    # this will be a list of strings
    warns = []
    
    def warn(s):
        warns.append(s)

    mp_glyph_set = set(mp_glyph_list)
    source_names = set([k for k in goadb['alias']])
    target_names = set([goadb['alias'][k] for k in goadb['alias']])
    
    not_used_source = source_names = mp_glyph_set
    # ~ warn(', '.join(list(not_used_source)))
    
    for k in goadb['alias']:
        if k != goadb['alias'][k]:
            if k in mp_glyph_set and goadb['alias'][k] in mp_glyph_set:
                warn("GOADB Ambiguous name, both %s and %s are in font." % (k, goadb['alias'][k]))
    return warns

    
    
# ------------------------------------------------------------------------------
# main glyph names translation functions:
# 31.01.2020 13:32:11
# ------------------------------------------------------------------------------
'''
1. source (metapost, eps) names to otf names
2. source names to pfb (Type1) names
3. pfb names to source names
'''


def source_to_otf(goadb, source_name):
    '''
    translate a source_name glyph name
    to the otf name
    using data in goadb structure
    '''
    res = goadb['alias'][source_name]
    return res
    
def source_to_pfb(goadb, source_name):
    '''
    translate a source_name glyph name
    to the pfb (Type1) name
    using data in goadb structure
    '''
    try:
        first = goadb['alias'][source_name]
    except:
        first = source_name

    try:
        second = goadb['xalias'][first]
    except:
        second = first
    return second

def pfb_to_source(goadb, pfb_name):
    '''
    translate a pfb_name glyph name
    to the source (eps, metapost) name
    using data in goadb structure
    '''
    # not ready yet
    return None



# ------------------------------------------------------------------------------
# glyph names transformation
# starting from the original version:
# ------------------------------------------------------------------------------

def glyph_name_to_type_one(goadb, glyph_name):
    '''
    Translate a metapost/eps glyph name
    to a target, Type1, glyph name
    using goadb structure a dictionary of three dictionaries of the form:

    {'alias': ..., 'unic': ..., 'xalias': ...}
    
    12.01.2020 20:59:40
    '''
    try:
        first = goadb['alias'][glyph_name]
    except:
        first = glyph_name

    try:
        second = goadb['xalias'][first]
    except:
        second = first
        
    return second
        
    



# ------------------------------------------------------------------------------
# renaming glyphs in the font
# according to goadb info
# this copy of the rename_glyphs function is not used yet
# (only the Python2 function is used in ffdkm.py)
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
        mess("GLYPH rename: 1")
        # made even more quiet, 11.04.2019 00:06:40:
        # ~ if quiet: print "almost done"
    for g in gly_lst:
        if '.' in g.glyphname:
            g.glyphname = sanit(g.glyphname)

    if unic:
        mess("  2")
    for n, g in list(gly_dic.items()):
        if unic:
            if n in alias:
                if n != alias[n]:
                    g.glyphname = sanit(alias[n])
                if n in unic:
                    ffunic = g.str
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
                        g.str = unic[n]
            else:
                if g.str > 0:
                    log_lib.warning("%-20s %04x not in GOADB" % (n, g.str))
                else:
                    log_lib.warning("%-20s not in GOADB" % n)
        else:
            n = tinas(g.glyphname) # `current' glyphname
            if n in alias and n != alias[n]:
                g.glyphname = sanit(alias[n])
                    
    if unic:
        mess("  3")
    for g in gly_lst:
        if '!!!' in g.glyphname:
           g.glyphname = tinas(g.glyphname)

    if unic:
        mess("  4 -- done")

def remove_redundant_glyphs(goadb):
    for k, v in list(gly_dic.items()):
        if k in goadb['unic']:
            if goadb['unic'][k] == -10:
                # ~ print 'key:', k, 'unic of key:', goadb['unic'][k], 'alias of key:', goadb['alias'][k]
                # ~ print 'glyph to be removed:', goadb['alias'][k]
                # ~ font.removeGlyph(goadb['alias'][k])
                # 19.08.2019 19:47:47:
                # if goadb['alias'][k] was unicode, the fontforge asked for an integer:
                font.removeGlyph(str(goadb['alias'][k]))
                
    
    
    




