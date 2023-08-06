#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''OTI --> ENC

   Genereates .enc and .map file based on information from .oti file
   
   Original Python 2 version converted to Python 3 on 16.03.2019 15:00:14,
   by Marek Ryćko
'''

__author__ = "Piotr Strzelczyk and Bogus/law Jackowski"
__copyright__ = "Copyright (c) 2017 by GUST e-foundry"
__credits__ = ["Piotr Strzelczyk", "Bogus/law Jackowski", "Piotr Pianowski"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Piotr Strzelczyk"
__email__ = "piotr@eps.gda.pl"
__status__ = "Beta"

import os
import sys
import string
from argparse import ArgumentParser

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

# ~ def write_warns(conf, vname):
    # ~ pass

    # ~ fval = open(os.path.join(conf['tfm_log_dir'], vname), 'w')
    # ~ for l in warns:
        # ~ fval.write("%s\n" % l)
    # ~ fval.close()

# ------------------------------------------------------------------------------
# processing elements (functions):
# ------------------------------------------------------------------------------
    

def fix_templates(templ, oti, pfb, inamei):
  job_name = re.sub('\.[^\.]+$', '', pfb)
  try:
      family_name = oti['FAMILY_NAME']
      font_name = oti['FONT_NAME']
  except:
      log_lib.error("No font names in OTI: %s" % inamei)
      family_name = job_name
      font_name = job_name
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
  for gly,inf in list(oti.items()):
    if ('CODE' in inf):
      c=int(inf['CODE'])
      if c>-1:
        if enc[c]=='.notdef':
           enc[c]=gly
        else:
           log_lib.error('Two gyphs with one code: %s and %s' % (enc[c],gly))
  res = "/%s[\n" % encn
  for gly in enc:
     res += "/%s\n" % gly
  res += "] def"
  return res
  
def create_map(tfm, fname, enci, enc, pfb):
  # pfb = re.sub('\.[^\.]+$', '.pfb', iname)
  res = '%s %s "%s ReEncodeFont" <%s <%s' % (tfm, fname, enci, enc, pfb)
  return res

def write_enc(enc_file_name, enc_data, templ):
    try:
        fenc = open(enc_file_name, 'w')
    except IOError:
        log_lib.critical("Couldn't open ENC file: %s" % enc_file_name)
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
        log_lib.critical("Couldn't open ENC file: %s" % enc_file_name)
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
        log_lib.critical("Couldn't open MAP file: %s" % map_file_name)
        return
    print(templ, file=fmap)
    print(map_line, file=fmap)
    fmap.close()
    
def append_map(map_file_name, map_line):
    try:
        fmap = open(map_file_name, 'a')
    except IOError:
        log_lib.critical("Couldn't open MAP file: %s" % map_file_name)
        return
    print(map_line, file=fmap)
    fmap.close()

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def main(conf, p):

    default = {
        # True or False:
        'quiet': False,
        # False, True or a file name:
        'verbose': False,
        # input:
        # a list of input oti filenames:
        'oti': [],
        # a list of input pfb filenames:
        'pfb': [],
        # a list of input tfm filenames (without extensions):
        'tfm': [],
        # output:
        # a list of output enc filenames:
        'enc': [],
        # a list of output enc filenames:
        'map': [],
        # False or a string denoting an identifier of a set of comment templates
        # the string may be something like 'TG'
        'comments': False,
    }
    
    
    par = {}
    par.update(default)
    par.update(p)



    ovname = par['verbose']
    quiet = par['quiet']

    # ~ quiet  = args.quiet
    # ~ ovname = args.verbose

    iname = [re.sub('\.[^\.]+$', '.oti', p.strip()) for p in par['oti']]
    otin = len(iname)

    if par['pfb']:
        pname = [p.strip() for p in par['pfb']]
    else:
        log_lib.critical("-pfb parameter is needed")
        
    if len(pname) != otin:
        log_lib.error("Number of OTIs and PFBs have to be the same: %d<>%d" % (otin, len(pname)))
        if len(pname) > otin:
            pname = pname[:otin] 
        else:
            pname = pname + [pname[0]] * (otin - len(pname))

    if par['tfm']:
        tname = [p.strip() for p in par['tfm']]
    else:
        log_lib.critical("-tfm parameter is needed")
        
    if len(tname) != otin:
        log_lib.error("Number of OTIs and TFMs have to be the same: %d<>%d" % (otin, len(tname)))
        if len(tname) > otin:
            tname = tname[:otin] 
        else:
            tname = tname + [tname[0]] * (otin - len(tname))
         
    if par['enc']:
        ename = [p.strip() for p in par['enc']]
    else:
        log_lib.critical("-enc parameter is needed")
        
    if len(ename) != otin:
        if len(ename) != 1:
            log_lib.error("Number of ENC names have to be the same as OTI (or 1): %d" % (len(ename),))
        if len(ename) > otin:
            ename = ename[:otin] 
        else:
            ename = [ename[0]] * otin

    ei_name = ['enc' + re.sub('(\-|\.enc)', '', e) for e in ename]

    if par['map']:
        mname = [p.strip() for p in par['map']]
    else:
        log_lib.critical("-map parameter is needed")
        
    if len(mname) != otin:
        if len(mname) != 1:
            log_lib.error("Number of MAP names have to be the same as OTI (or 1): %d" % (len(mname),))
        if len(mname) > otin:
            mname = mname[:otin] 
        else:
            mname = [mname[0]] * otin

    head  = par['comments']
    if head in TEMPLATE:
        templ = TEMPLATE[head]
    else:
        log_lib.warning("Unknown template: %s" % (head,))
        templ = {'enc': "", 'map': ""}


    #
    # Start of processing:
    #

    for i in range(otin):
        log_lib.info("OTI <", iname[i])
        # ~ oti_fnt, oti_gly, gly_lst = read_oti(os.path.join(conf['tfm_oti_dir'], iname[i]))
        oti = read_oti(os.path.join(conf['tfm_oti_dir'], iname[i]))
        oti_fnt = oti['font']
        oti_gly = oti['glyphs']
        glyn_lst = oti['list']
        # ~ oti = {'font': oti_fnt, 'glyphs': oti_gly, 'list': glyn_lst}

        font_name = fix_templates(templ, oti_fnt, pname[i], iname[i])
        
        # prepare enc and map filenames, including path
        # (moved from check_enc, write_enc, append_map, write_map functions,
        # where it was done twice)

        enc_file_name = os.path.join(conf['enc_dir'], ename[i])
        map_file_name = os.path.join(conf['map_dir'], mname[i])

        enc_data = create_enc(ei_name[i], oti_gly)
        if os.path.isfile(ename[i]):
            check_enc(enc_file_name, enc_data)
        else: 
            write_enc(enc_file_name, enc_data, templ['enc'])

        map_line = create_map(tname[i], font_name, ei_name[i], ename[i], pname[i])
        if os.path.isfile(mname[i]):
            append_map(map_file_name, map_line)
        else: 
            write_map(map_file_name, map_line, templ['map'])

    
    if 0:
        # no more used code; general logging is used
        # as of 05.03.2020 17:28:53
        if ovname:
            if ovname == True:
                ovname = re.sub('\.[^\.]+$', '.wrn', iname[0])
            ovname = ovname.strip()
            log_lib.info("WRN > %s" % ovname)
            if len(warns) > 0:
                pass
                # ~ write_warns(conf, ovname)





# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__ == '__main__':


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
    addarg('-v', '--verbose', nargs='?', const=True, help='Output warnings to the file')
    addarg('-q', '--quiet', action='store_true', help='Less messages')

    # ------------------------------------------------------------------------------
    args = argpars.parse_args()

    par = {
        'quiet': args.quiet,
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




