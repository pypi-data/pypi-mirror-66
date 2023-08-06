#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
enc_map_lib.py

The library of functions generating encoding and map files/strings
OTI --> ENC/MAP

Genereates .enc and .map file based on information from .oti file

Original Python 2 version converted to Python 3 on 16.03.2019 15:00:14,
by Marek Ryćko

20.04.2020 21:07:13
renamed from oti2enc3.py to enc_map_lib.py
'''

__author__ = 'Marek Ryćko, Piotr Strzelczyk and Bogusław Jackowski'
__copyright__ = 'Copyright (c) 2017, 2020 by GUST e-foundry'
__credits__ = ['Marek Ryćko', 'Piotr Strzelczyk', 'Bogusław Jackowski',
    'Piotr Pianowski']
__license__ = 'GPL'
__version__ = '0.2'
__maintainer__ = 'Marek Ryćko'
__email__ = 'marek@do.com.pl'
__status__ = 'Alpha'

import os
import sys
import string

# Algotype:
from algotype.ffdklib3 import *
# prints converted to log_lib function calls:
import algotype.log_lib as log_lib

# Templates of file headers (comments).
# The following items are appropriately substituted:
# #FAMILYNAME#, #FONTNAME#, #JOBNAME#

TEMPLATE = {
    'TG': {
        'enc':
      '''% This file belongs to the TeX Gyre collection of fonts. The work
% is released under the GUST Font License. See the respective
% MANIFEST*.txt and README*.txt files for the details.
% For the most recent version of this license see
% http://www.gust.org.pl/fonts/licenses/GUST-FONT-LICENSE.txt or
% http://tug.org/fonts/licenses/GUST-FONT-LICENSE.txt
%
% NOTE: all fonts of the TeX Gyre family share EXACTLY THE SAME
%       *.enc files.''',
        'map':
      '''% This file belongs to the TeX Gyre collection of fonts. The work is released
% under the GUST Font License. See the MANIFEST*.txt
% and README*.txt files for the details.
% For the most recent version of this license see
% http://www.gust.org.pl/fonts/licenses/GUST-FONT-LICENSE.txt or
% http://tug.org/fonts/licenses/GUST-FONT-LICENSE.txt
%
% This is the global map file for #FAMILYNAME#. It covers
% all available encodings.
'''
   },
    'LM': {
        'enc':
      '''% This file belongs to the Latin Modern collection of fonts. The work
% is released under the GUST Font License. See the respective
% MANIFEST*.txt and README*.txt files for the details.
% For the most recent version of this license see
% http://www.gust.org.pl/fonts/licenses/GUST-FONT-LICENSE.txt or
% http://tug.org/fonts/licenses/GUST-FONT-LICENSE.txt
%
% NOTE: all fonts of the Latin Modern family share EXACTLY THE SAME
%       *.enc files.''',
        'map':
      '''% This file belongs to the Latin Modern collection of fonts. The work is released
% under the GUST Font License. See the MANIFEST*.txt
% and README*.txt files for the details.
% For the most recent version of this license see
% http://www.gust.org.pl/fonts/licenses/GUST-FONT-LICENSE.txt or
% http://tug.org/fonts/licenses/GUST-FONT-LICENSE.txt
%
% This is the global map file for #FAMILYNAME#. It covers
% all available encodings.
'''
   },
}

# ------------------------------------------------------------------------------
# processing elements (functions):
# ------------------------------------------------------------------------------

def fix_templates(templ, oti, pfb):
    job_name = re.sub('\.[^\.]+$', '', pfb)
    
    # use family and font names from oti or use the basename of pfb name:
    try:
        family_name = oti['FAMILY_NAME']
        font_name = oti['FONT_NAME']
    except:
        # ~ log_lib.error('No font names in OTI: %s' % inamei)
        log_lib.error('No font names (FAMILY_NAME, FONT_NAME) in OTI structure')
        family_name = job_name
        font_name = job_name
    
    # replace the possible tags in 'enc' and 'map' templates (in situ):
        
    templ_ = re.sub('#FAMILYNAME#', family_name, templ['enc'])
    templ_ = re.sub('#FONTNAME#', font_name, templ_)
    templ_ = re.sub('#JOBNAME#', job_name, templ_)
    templ['enc'] = templ_
    
    templ_ = re.sub('#FAMILYNAME#', family_name, templ['map'])
    templ_ = re.sub('#FONTNAME#', font_name, templ_)
    templ_ = re.sub('#JOBNAME#', job_name, templ_)
    templ['map'] = templ_
    
    return font_name

def create_enc(encn, oti):
    enc = ['.notdef' for i in range(256)]
    for gly, inf in list(oti.items()):
        if ('CODE' in inf):
            c = int(inf['CODE'])
            if c > -1:
                if enc[c] == '.notdef':
                    enc[c] = gly
                else:
                    log_lib.error('Two gyphs with one code: %s and %s' % (enc[c], gly))
    res = '/%s[\n' % encn
    for gly in enc:
        res += '/%s\n' % gly
    res += '] def'
    return res
  
def create_map(tfm, fname, enci, enc, pfb):
    # pfb = re.sub('\.[^\.]+$', '.pfb', iname)
    # res = '%s %s "%s ReEncodeFont" <%s <%s' % (tfm, fname, enci, enc, pfb)
    # Python 3 style, 21.04.2020 00:07:32:
    res = f'{tfm} {fname} "{enci} ReEncodeFont" <{enc} <{pfb}'
    return res

def write_enc(enc_file_name, enc_data, templ):
    try:
        fenc = open(enc_file_name, 'w')
    except IOError:
        log_lib.critical('Couldn’t open ENC file: %s' % enc_file_name)
        return
    # those prints should be converted to file writes:
    # (mr, 07.03.2020 22:53:55)
    print(templ, file=fenc)
    print(enc_data, file=fenc)
    fenc.close()
    
def check_enc(enc_file_name, enc_data):
    try:
        fenc = open(enc_file_name, 'r')
    except IOError:
        log_lib.critical('Couldn’t open ENC file: %s' % enc_file_name)
        return
    nenc_lines = enc_data.split('\n')
    oenc_lines = []
    for line in fenc.readlines():
        line = re.sub('%.*$', '', line.rstrip()) # remove DOS/UNIX EOLs and comments
        if line!='':
            oenc_lines.append(line)
    if len(nenc_lines)!=len(oenc_lines):
        log_lib.warning('Encoding should have 256 entries (new %d, old %d)' % (len(nenc_lines)-2,len(oenc_lines)-2))
    for n, o in zip(nenc_lines, oenc_lines):
        if n!=o:
           log_lib.warning('!!! Encoding difference: %s <> %s !!!' % (n,o))
    fenc.close()

def write_map(map_file_name, map_line, templ):
    try:
        fmap = open(map_file_name, 'w')
    except IOError:
        log_lib.critical('Couldn’t open MAP file: %s' % map_file_name)
        return
    print(templ, file=fmap)
    print(map_line, file=fmap)
    fmap.close()
    
def append_map(map_file_name, map_line):
    try:
        fmap = open(map_file_name, 'a')
    except IOError:
        log_lib.critical('Couldn’t open MAP file: %s' % map_file_name)
        return
    print(map_line, file=fmap)
    fmap.close()

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def main(conf, p):

    default = {
        # inputs:
        'json_font': None,
        # the input oti filename:
        # not used any more:
        # 'oti': None,
        # the input pfb filename:
        #   like 'lmb10.pfb'
        'pfb': None,
        # the input tfm base filename (filename without extension):
        #   like 'cs-lmb10'
        'tfm': None,
        # ---------------------------
        # output:
        # the output enc filename:
        'enc': None,
        # the output internal enc name
        'enc_int': None,
        # the output map filename:
        'map': None,
        # ---------------------------
        # False or a string denoting an identifier of a set of comment templates
        # the string may be something like 'TG'
        'comments': False,
    }
    
    # prepare the dictionary of parameters as an update of the default:
    par = {}
    par.update(default)
    par.update(p)
    
    json_font = par['json_font']
    
    # ~ iname = re.sub('\.[^\.]+$', '.oti', par['oti'].strip())

    pname = par['pfb'].strip()
    tname = par['tfm'].strip()
    ename = par['enc'].strip()
    
    # preparing internal encoding name:
    
    # calculate internal name the origilal (Metatype1) way:
    ei_name = 'enc' + re.sub('(\-|\.enc)', '', ename)
    # take into consideration also the provided internal encoding name:
    enc_int = par['enc_int']
    
    # check if the just calculated and coming from the renaming structure
    # values of internal encodings are equal:
    if ei_name == enc_int:
        # everything is OK
        m = f"enc internal name = {repr(ei_name)} and " + \
            f"enc internal name from renaming structure = {repr(enc_int)} are equal"
        log_lib.debug(m)
    else:
        m = f"enc internal name = {repr(ei_name)} and " + \
            f"enc internal name from renaming structure = {repr(enc_int)} are NOT equal"
        log_lib.error(m)
    
    mname = par['map'].strip()

    head  = par['comments']
    if head in TEMPLATE:
        templ = TEMPLATE[head]
    else:
        log_lib.warning('Unknown template: %s' % (head,))
        templ = {'enc': '', 'map': ''}

    #
    # Start of processing:
    #

    if 0:
        # no more duplicated parsing of oti
        # will read the data from json_font
        
        # read the OTI file and parse it to a structure
        # (it should not be done here; just the already parsed
        # structure should be passed as a parameter; 20.04.2020 23:23:54)
        log_lib.info('OTI <', iname)
        # ~ oti_fnt, oti_gly, gly_lst = read_oti(os.path.join(conf['tfm_oti_dir'], iname))
        oti = read_oti(os.path.join(conf['tfm_oti_dir'], iname))
        oti_fnt = oti['font']
        oti_gly = oti['glyphs']
        glyn_lst = oti['list']
    else:
        # reading oti data from json font:
    
        oti_fnt = json_font['oti_par']
        oti_gly = json_font['oti_glyphs']
        glyn_lst = json_font['glyph_list']
    
    # ~ oti = {'font': oti_fnt, 'glyphs': oti_gly, 'list': glyn_lst}

    # change “in place” the templates, using info from oti
    # and possibly from pfb name (pname)
    # also possibly reporting error using iname as oti file name:
    font_name = fix_templates(templ, oti_fnt, pname)
    
    # prepare enc and map filenames, including path
    # (moved from check_enc, write_enc, append_map, write_map functions,
    # where it was done twice)

    enc_file_path = os.path.join(conf['enc_dir'], ename)
    map_file_path = os.path.join(conf['map_dir'], mname)

    enc_data = create_enc(ei_name, oti_gly)
    if os.path.isfile(ename):
        check_enc(enc_file_path, enc_data)
    else: 
        write_enc(enc_file_path, enc_data, templ['enc'])

    map_line = create_map(tname, font_name, ei_name, ename, pname)
    if os.path.isfile(mname):
        append_map(map_file_path, map_line)
    else: 
        write_map(map_file_path, map_line, templ['map'])


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    
    # the following code is planned to be removed
    # as of 20.04.2020 22:24:58:

    from argparse import ArgumentParser

    argpars = ArgumentParser(description='OTI -> ENC/MAP converter',
        fromfile_prefix_chars='@')
    addarg = argpars.add_argument
    addarg('oti', nargs='+', help='Input OTI filename(s)')
    #addarg('-o', '--oti', action='append', help='Input OTI filename')
    addarg('-e', '--enc', action='append', help='Generated ENC file(s)')
    addarg('-m', '--map', action='append', help='Generated MAP file(s)')
    addarg('-p', '--pfb', action='append', help='PFB filename(s)  (for MAP)')
    addarg('-t', '--tfm', action='append', help='TFM filename(s)  (for MAP)')
    addarg('-c', '--comments', nargs='?', const=False, 
      help='Header coments template (avaiable: %s)' % (', '.join(list(TEMPLATE.keys()))))

    # ------------------------------------------------------------------------------
    args = argpars.parse_args()

    par = {
        'verbose': args.verbose,
        'oti': args.oti,
        'pfb': args.pfb,
        'tfm': args.tfm,
        'enc': args.enc,
        'map': args.map,
        'comments': args.comments,
    }

    # ------------------------------------------------------------------------------

    main(par)
    exit()




