#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Rename glyph names inf an LM-style feature file

13.12.2019 21:46:57
'''

__author__ = "Piotr Strzelczyk and Bogus/law Jackowski"
__copyright__ = "Copyright (c) 2017 by GUST e-foundry"
__credits__ = ["Piotr Strzelczyk", "Bogus/law Jackowski", "Piotr Pianowski"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Piotr Strzelczyk"
__email__ = "piotr@eps.gda.pl"
__status__ = "Beta"

# standard library:
import os
import sys
# ~ import string
import re
# ~ import textwrap
# for dictionaries with default values:
# ~ from collections import defaultdict

from algotype.parse_config import ll_to_sl, pll_to_pdl, repr_struct
import algotype.log_lib as log_lib


def parse_line(s):
    '''
    Parse a single line string s and return a list of lexical units.
    '''
    

def fea_parse(s):
    '''
    parse fea file (at the level of simple lexical analysis)
    and return a list of lists of lexical units
    '''
    
    ll = s.splitlines()
    log_lib.debug(len(ll))
    
    
    # lexical grammar; pattern list list:

    pll = [
        ['comment', r'\#.*$'],

        ['id', r'\@([a-zA-Z\_][a-zA-Z0-9\_]*)'],
        ['name', r'([a-zA-Z\_][a-zA-Z0-9\_\/]*)'],
        ['rest', r'([^@a-zA-Z\_]+)'],

    ]
        
    pdl = pll_to_pdl(pll)

    sl = ll_to_sl(ll, pdl)
        
    return sl
    
def goadb_parse(s):
    '''
    Parse the goadb file and return a minimal logical structure of it.
    '''
    
    sl = s.splitlines()
    
    # new list:
    nl = [s for s in sl if not bad(s)]
    for line in nl[:50]:
        # ~ log_lib.debug(line)
        pass
        
    # split lines at the whitespace:
    
    # sTructures list:
    tl = []
    for line in nl:
        spl = line.split()
        tl.append(spl)
        
    for line in tl[:50]:
        # ~ log_lib.debug(line)
        pass
    log_lib.debug(len(tl))
        
    # pairs list:
    pl = []
    for line in tl:
        if line[0] != line[1]:
            # ~ log_lib.debug(line[0])
            pass
            # ~ pl.append([line[0], line[1]])
        pl.append([line[0], line[1]])

    for line in pl[:50]:
        # ~ log_lib.debug(line)
        pass
    log_lib.debug(len(pl))
    
    # metapostowe nazwy:
    # [tTdD]macronbelow
    
    # analysis of the relations between names, both ways
    
    # collect relations from metapost names to otf names and back
    mo_rel = {}
    om_rel = {}
    for l in pl:
        m = l[1]
        o = l[0]
        if 'linebelow' in o or 'linebelow' in m:
            log_lib.debug('line...:', o, m)
        if o in om_rel:
            om_rel[o].append(m)
        else:
            om_rel[o] = [m]
            
        if m in mo_rel:
            mo_rel[m].append(o)
        else:
            mo_rel[m] = [o]
    # relations collected
    
    # analyse the relations
    log_lib.debug('mpost --> oti relation length = %d' % len(mo_rel))
    log_lib.debug('oti --> mpost relation length = %d' % len(om_rel))
    
    # show interesting entries:
    
    def repr_list(l):
        return ', '.join([str(s) for s in l])
    
    for k, v in mo_rel.items():
        # consider showing the relation at the point k:
        if len(v) == 1 and v[0] == k:
            # identity here; not interesting
            pass
        else:
            if len(v) != 1:
            # ~ if len(v) == 1:
                log_lib.debug('mpost --> oti relation %s --> %s' % (k, repr_list(v)))

    for k, v in om_rel.items():
        # consider showing the relation at the point k:
        if len(v) == 1 and v[0] == k:
            # identity here; not interesting
            pass
        else:
            if len(v) != 1:
            # ~ if len(v) == 1:
                log_lib.debug('oti --> mpost relation %s --> %s' % (k, repr_list(v)))
    
    
    # translate pairs to a dictionary:
    goadb = {}
    for l in pl:
        o, m = l
        if m in ('Dmacronbelow', 'dmacronbelow', 'Tmacronbelow', 'tmacronbelow'):
            pass
            log_lib.debug('skipping %s: %s' % (o, m))
        else:
            if l[0] in goadb:
                # ~ log_lib.debug('duplicate entry: [%s: %s], [%s: %s]' % (l[0], goadb[l[0]], l[0], l[1]))
                pass
            goadb[l[0]] = l[1]

    for k, v in goadb.items():
        # ~ log_lib.debug('%s: %s' % (k, v))
        pass
    log_lib.debug(len(goadb))
    
    return goadb
    
def bad(s):
    '''
    Analyse the string s and return a boolean information if it is “bad”.
    
    “Bad” is a whitespace line or a comment line
    '''
    pat = r'(^\s*$|^\s*\#)'
    patc = re.compile(pat)
    mo = patc.match(s)
    return True if mo else False
    
def translate_structure_list(goadb, structure_list):
    '''
    Translate a structure representing a fea file, applying goadb structure.
    
    replace glyph names in structure_list, using a dictionary goadb
    '''
    
    for stru in structure_list:
        for u in stru['lul']:
            # u is a lexical unit
            
            if u['k'] == 'name':
                # possibly translate
                # ~ log_lib.debug(u)
                if u['v'] in goadb:
                    # ~ log_lib.debug('translating: %s --> %s' % (u['v'], goadb[u['v']]))
                    u['v'] = goadb[u['v']]
                    pass
        
    return structure_list
    
def serialize_structure_list(structure_list):
    '''
    Serialize structure list as a string.
    '''
    # collect string list:
    sl = [''.join([u['v'] for u in line['lul']]) for line in structure_list]
    return '\n'.join(sl)

def main():
    
    # read and parse fea file:
    
    # directory name:
    # ~ dnf = '/1/mini/programowanie/0tematy/fonty/002_nowy_etap_z_poszerzonym_językiem_programowania_konfiguracji/50_out/2019_12_10_22_00/fea'
    dnf = '/1/mini/programowanie/0tematy/fonty/002_nowy_etap_z_poszerzonym_językiem_programowania_konfiguracji/40_inp/fea'
    
    # file name:
    # ~ fn = 'lmr10.fea'
    # ~ fn = '_csc_fea.dat'
    fn = '_tt_fea.dat'
    # ~ fn = '_all_fea.dat'
    # ~ fn = '_all_fea_test.dat'
    
    # path name:
    pn = os.path.join(dnf, fn)
    
    # ~ log_lib.debug(pn)
    
    # open and read the fea file:
    with open(pn, 'r') as fh:
        s = fh.read()
        
    # ~ log_lib.debug(s)
    
    structure_list = fea_parse(s)
    
    for lt in structure_list:
        # ~ log_lib.debug(repr_struct(lt))
        pass
    
    # read and parse goadb file:
    
    dn = '/1/mini/programowanie/0tematy/fonty/002_nowy_etap_z_poszerzonym_językiem_programowania_konfiguracji/40_inp/goadb'
    
    # file name:
    fn = 'goadb999.nam'
    
    # path name:
    pn = os.path.join(dn, fn)
    
    # ~ log_lib.debug(pn)
    
    # open and read the fea file:
    with open(pn, 'r') as fh:
        s = fh.read()
        
    # ~ log_lib.debug(s)
    
    goadb = goadb_parse(s)
    
    translate_structure_list(goadb, structure_list)
    
    for stru in structure_list:
        # ~ log_lib.debug(stru)
        pass
    
    s = serialize_structure_list(structure_list)
    # ~ log_lib.debug(s)
    
    # file name:
    # ~ fn = 'lmr10.mpost.fea'
    # ~ fn = '_all_fea.mpost.dat'
    # ~ fn = '_csc_fea.mpost.dat'
    fn = '_tt_fea.mpost.dat'
    
    # path name:
    pn = os.path.join(dnf, fn)
    
    # ~ log_lib.debug(pn)
    
    # open and read the fea file:
    with open(pn, 'w') as fh:
        fh.write(s)



if __name__ == '__main__':
    main()