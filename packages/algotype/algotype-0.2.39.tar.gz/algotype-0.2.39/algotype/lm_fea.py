#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''Genereate feature file (.fea) based on information from .oti file; LM-style.

'''

__author__ = "Marek Ryćko"
__copyright__ = "Copyright (c) 2019 by GUST e-foundry"
__credits__ = ["Marek Ryćko", "Bogusław Jackowski"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Marek Ryćko"
__email__ = "marek@do.com.pl"
__status__ = "Alpha"

# standard library:
import os
import sys
import string
import re
import math
# ~ import textwrap
# for dictionaries with default values:
from collections import defaultdict

# Algotype library:
# reading and (some) parsing of oti file:
import algotype.ffdklib3 as ffdklib3
import algotype.json_font_lib as json_font_lib
# prints converted to log_lib function calls:
import algotype.log_lib as log_lib

template_patern = "????"

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def read_template(tname):
    try:
        # ftpl = file(tname, 'r')
        # 21.02.2019 03:30:58
        fh = open(tname, 'r')
    except IOError:
        log_lib.critical("Couldn't find TEMPLATE file: %s" % tname)
        return ''
    s = fh.read()
    # ~ s = s.replace()
    return s

# ------------------------------------------------------------------------------
def round_away_from_zero(n):
    if n >= 0:
        res = math.ceil(n)
    else:
        x = -n
        c = math.ceil(x)
        res = -c
    return res

# ------------------------------------------------------------------------------
# collect feature data:
# ------------------------------------------------------------------------------
def prepare_fea_data(oti_font):
    
    of = oti_font
    r = {}
    r['font_name'] = of['FONT_NAME']
    r['weight'] = of['WEIGHT']
    r['italic_angle'] = of['ITALIC_ANGLE']
    # for OS/2 table:
    # ~ if ($1~/FontBBox/)  {WDES=round($3); WASC=round($5)}
    
    r['x_height'] = of['XHEIGHT']
    r['cap_height'] = of['CAPHEIGHT']
    r['ascender'] = of['ASCENDER']
    r['descender'] = of['DESCENDER']
    
    return r


def prepare_kern_info(oti_gly):

    ki = json_font_lib.kern_info(oti_gly)
    return ki

def prepare_size_data():
    size_data = {}
    # Roman
    size_data["lmr5"]     = "1 50 30 55 Regular"
    size_data["lmr6"]     = "1 60 55 65 Regular"
    size_data["lmr7"]     = "1 70 65 75 Regular"
    size_data["lmr8"]     = "1 80 75 85 Regular"
    size_data["lmr9"]     = "1 90 85 95 Regular"
    size_data["lmr10"]    = "1 100 95 110 Regular"
    size_data["lmr12"]    = "1 120 110 140 Regular"
    size_data["lmr17"]    = "1 172 140 240 Regular"
    size_data["lmri7"]    = "2 70 40 75 Italic"
    size_data["lmri8"]    = "2 80 75 85 Italic"
    size_data["lmri9"]    = "2 90 85 95 Italic"
    size_data["lmri10"]   = "2 100 95 110 Italic"
    size_data["lmri12"]   = "2 120 110 240 Italic"
    size_data["lmro8"]    = "1 80 40 85 Regular"
    size_data["lmro9"]    = "1 90 85 95 Regular"
    size_data["lmro10"]   = "1 100 95 110 Regular"
    size_data["lmro12"]   = "1 120 110 140 Regular"
    size_data["lmro17"]   = "1 172 140 240 Regular"
    size_data["lmb10"]    = "1 100 50 200 Regular"
    size_data["lmbo10"]   = "2 100 50 200 Oblique"
    size_data["lmbx5"]    = "3 50 30 55 Bold"
    size_data["lmbx6"]    = "3 60 55 65 Bold"
    size_data["lmbx7"]    = "3 70 65 75 Bold"
    size_data["lmbx8"]    = "3 80 75 85 Bold"
    size_data["lmbx9"]    = "3 90 85 95 Bold"
    size_data["lmbx10"]   = "3 100 95 110 Bold"
    size_data["lmbx12"]   = "3 120 110 240 Bold"
    size_data["lmbxi10"]  = "4 100 50 200 Bold Italic"
    size_data["lmbxo10"]  = "2 100 50 200 Bold"
    size_data["lmcsc10"]  = "1 100 50 200 Regular"
    size_data["lmcsco10"] = "2 100 50 200 Oblique"
    size_data["lmdunh10"] = "1 100 50 200 Regular"
    size_data["lmduno10"] = "2 100 50 200 Oblique"
    size_data["lmu10"]    = "1 100 50 200 Regular"
    # Sans
    size_data["lmss8"]    = "1 80 40 85 Regular"
    size_data["lmss9"]    = "1 90 85 95 Regular"
    size_data["lmss10"]   = "1 100 95 110 Regular"
    size_data["lmss12"]   = "1 120 110 140 Regular"
    size_data["lmss17"]   = "1 172 140 240 Regular"
    size_data["lmssbx10"] = "3 100 50 200 Bold"
    size_data["lmssbo10"] = "4 100 50 200 Bold Oblique"
    size_data["lmssdc10"] = "1 100 50 200 Demi Cond"
    size_data["lmssdo10"] = "2 100 50 200 Demi Cond Oblique"
    size_data["lmsso8"]   = "2 80 40 85 Oblique"
    size_data["lmsso9"]   = "2 90 85 95 Oblique"
    size_data["lmsso10"]  = "2 100 95 110 Oblique"
    size_data["lmsso12"]  = "2 120 110 140 Oblique"
    size_data["lmsso17"]  = "2 172 140 240 Oblique"
    size_data["lmssq8"]   = "1 80 40 160 Regular"
    size_data["lmssqbo8"] = "4 80 40 160 Bold Oblique"
    size_data["lmssqbx8"] = "3 80 40 160 Bold"
    size_data["lmssqo8"]  = "2 80 40 160 Oblique"
    # Typewriter
    size_data["lmtcsc10"] = "1 100 50 200 Regular"
    size_data["lmtcso10"] = "2 100 50 200 Oblique"
    size_data["lmtk10"]   = "3 100 50 200 Bold"
    size_data["lmtko10"]  = "4 100 50 200 Bold Oblique"
    size_data["lmtl10"]   = "1 100 50 200 Regular"
    size_data["lmtlo10"]  = "2 100 50 200 Oblique"
    size_data["lmtlc10"]  = "1 100 50 200 Regular"
    size_data["lmtlco10"] = "2 100 50 200 Oblique"
    size_data["lmtt8"]    = "1 80 40 85 Regular"
    size_data["lmtt9"]    = "1 90 85 95 Regular"
    size_data["lmtt10"]   = "1 100 95 110 Regular"
    size_data["lmtt12"]   = "1 120 110 240 Regular"
    size_data["lmtti10"]  = "2 100 50 200 Italic"
    size_data["lmtto10"]  = "1 100 50 200 Regular"
    size_data["lmvtk10"]  = "3 100 50 200 Bold"
    size_data["lmvtko10"] = "4 100 50 200 Bold Oblique"
    size_data["lmvtl10"]  = "1 100 50 200 Regular"
    size_data["lmvtlo10"] = "2 100 50 200 Oblique"
    size_data["lmvtt10"]  = "1 100 50 200 Regular"
    size_data["lmvtto10"] = "2 100 50 200 Oblique"

    sd = {}
    for k in size_data:
        sd[k] = size_data[k].split(maxsplit=4)

    return sd
    
def calculate_scenders(oti_gly, glyn_lst):
    '''
    Calculate vertical bounding box of a font: ascender and descender
    
    calculate the maximum (extremum) values of glyph scenders
    for all glyphs in the font
    
    the oti_gly is like this:
    
    "Abrevehookabove": {
            "codepoint": null,
            "glyph_name": "Abrevehookabove",
            "metrics": {
                "width": 750,
                "textheight": 1127,
                "textdepth": 0
            },
            ...
            "meta": {
                "BoundingBox": [
                    32,
                    0,
                    717,
                    1127
                ],
                "HiResBoundingBox": [
                    32,
                    0,
                    717,
                    1127
                ],
            ...
            },
    ...
    }
    
    
    '''
    
    json_glyphs = json_font_lib.glyphs_json(oti_gly, glyn_lst, None)
    
    max_a = None
    min_d = None
    for g in json_glyphs.values():
        a = g['metrics']['textheight']
        d = g['metrics']['textdepth']
        if max_a is None or max_a < a:
            max_a = a
        if min_d is None or min_d > d:
            min_d = d
    return max_a, min_d


# ------------------------------------------------------------------------------
# serialization functions:
# ------------------------------------------------------------------------------
def data_group(gtype, gname, contents):
    '''
    Create a feature file data group, like feature or table.
    
    for given:
     -- gtype: group type string (like ‘feature’ or ‘table’)
     -- gname: group name (like ‘kern’, ‘size’, ‘hhea’)
     -- contents: a list of contents single-line strings (no leading
        indents and no trailing semicolons)
    create and return a data group string
    '''
    # local configuration:
    indent = ' ' * 2
    
    cont_list = [indent + s + ';' for s in contents]
    prefix = '%s %s {' % (gtype, gname)
    postfix = '} %s;' % (gname,)
    
    group_list = [prefix] + cont_list + [postfix]
    group = '\n'.join(group_list)
    
    return group
    
def kern_info_to_kern_lines(ki):
    '''
    Translate a kern info structure to a list of lines.
    
    Take a kern info structure of the form:
    ki = {
        'A': {'C': -27.778, 'Cacute': -27.778, 'Ccaron': -27.778, ...}
        'a': ...
        ...
    }
    And return a list of strings in the format:
        'pos name1 name2 kern'
    '''
    kern_list = []
    for g1 in ki:
        # g1 is a left glyph name of some kern pair
        for g2 in ki[g1]:
            # we define a kern pair between g1 and g2
            value = ki[g1][g2]
            rounded_value = round(ki[g1][g2])
            kern_list.append('pos %s %s %d' % (g1, g2, rounded_value))
    return kern_list
            
    
def kern_group(kern_lines):
    '''
    Return a feature kern string.
    
    for given kern_lines (strings of kern info)
    serialize kern data and return as a string
    '''
    const_kern_lines = [
        'script latn',
        'language AZE',
        'language CRT',
        'language MOL',
        'language NLD',
        'language PLK',
        'language ROM',
        'language TRK',
    ]
    
    # ~ res = data_group('feature', 'kern', kern_lines + const_kern_lines)
    # 28.12.2019 19:25:19:
    # no kerns here; they are directly put into fontforge
    res = data_group('feature', 'kern', const_kern_lines)
    return res
    

def size_group(sd):
    '''
    Return a feature size string.
    
    for given five parameters return
    a three lines of the shape similar to:
        parameters 100 1 95 110
        sizemenuname 3 "Regular"
        sizemenuname 1 "Regular"
    
    '''
    par_line = 'parameters %s %s %s %s' % (sd[1], sd[0], sd[2], sd[3])
    size_line_one = 'sizemenuname 3 "%s"' % (sd[4],)
    size_line_two = 'sizemenuname 1 "%s"' % (sd[4],)
    
    res = data_group('feature', 'size', [par_line, size_line_one, size_line_two])
    return res

def hhea_group(asc, desc):
    hhea_strings = [
        'Ascender %s' % str(round(asc)),
        'Descender %s' % str(round(desc)),
        'LineGap %s' % '0',
    ]
    res = data_group('table', 'hhea', hhea_strings)
    return res

def os2_group(oti_fnt, win_asc, win_desc):
    
    # --------------------------------------------------------------------------
    # collect and calculate data:
    
    fea_data = prepare_fea_data(oti_fnt)
    # ~ log_lib.debug('fea_data =', fea_data)
    
    fs_type = 12

    # calculate typo ascender, typo descender and line gap:

    '''
    excerpt from the original afm2fdk.awk:
    
    # 26.02.2007: these lines:
    # print "  TypoDescender " DES  ";" > AFM ".fea"
    # print "  TypoLineGap   " max(0,min(1200-(ASC-DES),200)) ";" > AFM ".fea"
    # caused the following warning:
    # MAKEOT~1.EXE [WARNING] <LMRoman10-Dunhill> The feature file OS/2 overrides
    # TypoAscender and TypoDescender do not sum to the font bbox size!
    # MAKEOT~1.EXE [NOTE] Wrote new font file 'LMRoman10-Dunhill.otf'.
    # hence circumventing:
    print "  TypoDescender " min(0,max(DES,ASC-1000)) ";" > AFM ".fea"
    print "  TypoLineGap   " 200  ";" > AFM ".fea"
    '''
    
    ascender = float(fea_data['ascender'])
    descender = float(fea_data['descender'])
    asc = max(ascender, 1000 + descender)
    # ~ desc = max(ascender, 1000 + descender)
    desc = min(0, max(descender, ascender - 1000))
    # ~ log_lib.debug(ascender, descender, asc, desc)
    
    # ~ TypoAscender
    # used to be round:
    # typo_ascender = round(asc)
    # typo_descender = round(desc)
    # round changed to rounding away from zero 28.01.2020 15:20:13:
    typo_ascender = round_away_from_zero(asc)
    typo_descender = round_away_from_zero(desc)
    
    # original formula from afm2fdk.awk:
    # TypoLineGap   " max(0,min(1200-(ASC-DES),200))
    typo_line_gap = 200
    # ~ log_lib.debug(typo_ascender, typo_descender, typo_line_gap)
    
    '''
    excerpt from the original afm2fdk.awk, regarding the new way
    of calculating the three parameters:
    
    # In Dunhill, it yields
    #     TypoAscender 972
    #     TypoDescender -28
    #     TypoLineGap 200
    # instead of (seemingly more reasonable):
    #     TypoAscender 972
    #     TypoDescender -194
    #     TypoLineGap 34
    '''
    
    x_height = oti_fnt['XHEIGHT']
    cap_height = oti_fnt['CAPHEIGHT']
    # those two are strings
    # ~ log_lib.debug(repr(x_height), repr(cap_height))
    x_h = round(float(x_height))
    cap_h = round(float(cap_height))
    
    
    # win ascent and win descent are almost already calculated
    # for the hhea table, as: win_asc, win_desc,
    # but win descent will need to be made positive (not reversed?)
    
    win_ascent = round_away_from_zero(win_asc)
    win_descent = round_away_from_zero(abs(win_desc))
    
    # --------------------------------------------------------------------------
    # prepare strings:
    os2_strings = [
        'FSType %s' % str(fs_type),
        'TypoAscender %s' % str(typo_ascender),
        'TypoDescender %s' % str(typo_descender),
        'TypoLineGap %s' % str(typo_line_gap),
        'XHeight %s' % str(x_h),
        'CapHeight %s' % str(cap_h),
        'winAscent %s' % str(win_ascent),
        'winDescent %s' % str(win_descent),
    ]

    res = data_group('table', 'OS/2', os2_strings)
    return res


# ------------------------------------------------------------------------------

def main(inp, template_name, output, fb, q=True):
    global quiet
    quiet = q

    # ~ log_lib.debug(inp, template_name, output)
    iname = inp.strip()
    iname = re.sub(r'\.[^\.]+$', '.oti', iname)
    oname = output
    
    # to respect the ”quiet” parameter:
    log_lib.info("OTI < " + iname)

    oti = ffdklib3.read_oti(iname)
    oti_fnt = oti['font']
    oti_gly = oti['glyphs']
    glyn_lst = oti['list']
    
    # ~ log_lib.debug(oti_fnt)
    # ~ log_lib.debug(oti_gly)
    
    par = json_font_lib.font_parameters_to_json(oti_fnt)
    # ~ log_lib.debug(par['em'])
    # ~ log_lib.debug(par)


    # prepare the name of the feature template file
    if template_name:
        template_name = template_name.strip()
        # to respect the “quiet” parameter:
        log_lib.info("TPL < %s" % template_name)
        template = read_template(template_name)
    # template is a (potentially multiline) string

    # ~ log_lib.debug(template)
    
    version = oti_fnt['VERSION']
    # ~ version = oti_fnt.keys()
    
    # ~ log_lib.debug(version)

    prefix = template.replace(template_patern, version)
    # remove leading and trailing whiteline (in fact trailing only)
    prefix = prefix.strip()

    # ~ log_lib.debug(prefix)
    # prefix is a beginning part of the template file being generated
    # with a font version already replaced
    
    for k in oti_fnt:
        # ~ log_lib.debug('%s: %s' % (k, oti_fnt[k]))
        pass
    

    # --------------------------------------------------------------------------
    # feature kern part:

    ki = prepare_kern_info(oti_gly)
    # ~ log_lib.debug(ki.keys())
    # ~ log_lib.debug(ki['A'])
    
    kern_list = kern_info_to_kern_lines(ki)
    # ~ for l in kern_list:
        # ~ log_lib.debug(l)
    
    kern_group_string = kern_group(kern_list)
    # ~ log_lib.debug(kern_group_string)
    
    # count the number of kerns:
    if 0:
        kern_count = 0
        for k1 in ki:
            for k2 in k1:
                kern_count += 1
        log_lib.debug('There are %d kerns.' % kern_count)

    # --------------------------------------------------------------------------
    # feature size part:

    sd = prepare_size_data()
    this_sd = sd[fb]
    # ~ log_lib.debug(this_sd)

    if 0:
        for k in sd:
            # ~ log_lib.debug('%s: %s' % (k, sd[k]))
            pass
    size_group_string = size_group(this_sd)
    # ~ log_lib.debug(size_group_string)
    # --------------------------------------------------------------------------
    # table hhea part:
    win_asc, win_desc = calculate_scenders(oti_gly, glyn_lst)
    # ~ log_lib.debug(win_asc, win_desc)
    hhea_group_string = hhea_group(win_asc, win_desc)
    # ~ log_lib.debug(hhea_group_string)
    # --------------------------------------------------------------------------
    # table OS/2 part:
    
    os2_group_string = os2_group(oti_fnt, win_asc, win_desc)
    # ~ log_lib.debug(os2_group_string)
    # --------------------------------------------------------------------------
    # create the resulting fea string:
    
    # a list of multiline-strings:
    fea_strings = [
        prefix,
        kern_group_string,
        size_group_string,
        hhea_group_string,
        os2_group_string,
    ]
    fea_string = '\n\n'.join(fea_strings)
    
    # ~ log_lib.debug(fea_string)
    
    # write the resulting fea_string:
    with open(output, 'w') as fh:
        fh.write(fea_string)
    
    return fea_string
    
    # --------------------------------------------------------------------------

    if 0:
        # prepare the name of the output feature file:
        # in future it should be defined in the config file
        # and generate the fea file for this output filename:
        if oname:
            # the output is specified (may be empty or just whitespace):
            oname = oname.strip()
            # if oname == '':
            if len(oname) == 0:
                oname = iname.replace('.oti', '.fea', '')
            # to respect the “quiet” parameter:
            log_lib.info("FEA > %s" % oname)
            s = fea_string_prepare(oti_gly, template)
            fea_write(s, oname)
            
