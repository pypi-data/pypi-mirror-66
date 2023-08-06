#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''A library of functions for collecting and verifying kerns from various sources.

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
import regex as re
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


def prepare_kern_info(oti_gly):

    ki = json_font_lib.kern_info(oti_gly)
    return ki


# ------------------------------------------------------------------------------

def read_oti_kerns_mt(oti_str):
    '''Read kerns from oti file, the Metatype1 style
    '''
    sl = oti_str.splitlines()

    oti_fnt = {} 
    oti_gly = {} 
    gly_lst = []
    for line in sl:
        line = re.sub(' *#.*$', '', line)
        if line == '': continue
        if (line.find('GLY ')==0):
           linem = re.match(r'^GLY[ \t]+([A-Za-z0-9\._]+)[ \t]+([A-Z_\-]+)[ \t]+(.+)$', line)
           if linem:
               gly=linem.group(1)
               if gly not in oti_gly:
                   oti_gly[gly]={}
                   gly_lst.append(gly)
               if linem.group(2)=='KPX':
                   if 'KPX' not in oti_gly[gly]:
                       oti_gly[gly]['KPX'] = []
                   oti_gly[gly]['KPX'].append(linem.group(3).split())
               else:
                   if linem.group(2) not in oti_gly[gly]:
                       oti_gly[gly][linem.group(2)] = linem.group(3)
                   else:
                       log_lib.warning("Duplicate atribute in OTI:\n  %s" % line)
                       pass
           else:
               log_lib.warning("Unrecognized line in OTI:\n  %s" % line)
    return oti_gly



# ------------------------------------------------------------------------------
'''
The kern info is a(n ordered) dictionary of the shape:
    {
        ('gl1', 'gr1'): k1,
        ...
    }
where gl1, gr1 are glyph names
and k1 is a kern value (a real/float number)

'''


def afm_kerns(afm_str):
    '''prepare a kern information from afm string
    
    '''
    sl = afm_str.splitlines()
    # collect the kern info:
    ki = {}
    for s in sl:
        # fields list:
        fl = s.split()
        if fl[0] == 'KPX':
            # this is the kern info line:
            if len(fl) != 4:
                log_lib.error('wrong KPX line in AFM file: %s' % s)
            ki[(fl[1], fl[2])] = fl[3]
        elif 'KPX' in s:
            log_lib.debug('some other KPX in AFM line: %s' % s)
        elif 'kpx' in s:
            log_lib.debug('some kpx in AFM line: %s' % s)
            # ~ pass
    log_lib.debug('liczba kernów w pliku AFM: %d' % len(ki))
    return ki

def oti_kerns(oti_str):
    '''prepare a kern information from afm string
    
    '''
    sl = oti_str.splitlines()
    # collect the kern info:
    ki = {}
    for s in sl:
        # fields list:
        fl = s.split()
        if fl[0] == 'GLY' and fl[2] == 'KPX':
            # this is the kern info line:
            if len(fl) != 5:
                log_lib.error('wrong KPX line in OTI file: %s' % s)
            ki[(fl[1], fl[3])] = fl[4]
        elif 'KPX' in s:
            log_lib.debug('some other KPX in OTI line: %s' % s)
        elif 'kpx' in s:
            log_lib.debug('some kpx in OTI line: %s' % s)
            # ~ pass
    log_lib.debug('liczba kernów w pliku OTI: %d' % len(ki))
    return ki
        
def oti_kerns(oti_str):
    '''prepare a kern information from afm string
    
    '''
    sl = oti_str.splitlines()
    # collect the kern info:
    kl = []
    bad = []
    ki = {}
    logl = []
    for i, s in enumerate(sl):
        # fields list:
        if 'KPX' in s:
            # ~ kl.append(s)


            # fields list:
            fl = s.split()
            if fl[0] == 'GLY' and fl[2] == 'KPX':
                # this is the kern info line:
                if len(fl) != 5:
                    log_lib.error('wrong KPX line in OTI file: %s' % s)
                if (fl[1], fl[3]) in ki:
                    if ki[(fl[1], fl[3])] != fl[4]:
                        log_lib.error('inconsistent:', (fl[1], fl[3]), ki[(fl[1], fl[3])], fl[4])
                        logl.append('inconsistent: %s %s %s' % (str((fl[1], fl[3])), str(ki[(fl[1], fl[3])]), str(fl[4])))
                        bad.append(s)
                    else:
                        kl.append(s)
                        logl.append('    repeated: %s %s %s' % (str((fl[1], fl[3])), str(ki[(fl[1], fl[3])]), str(fl[4])))
                else:
                    ki[(fl[1], fl[3])] = fl[4]
            else:
                pass


            # ~ log_lib.debug('some other KPX in OTI line: %s' % s)
        # ~ elif 'kpx' in s:
            # ~ log_lib.debug('some kpx in OTI line: %s' % s)
            # ~ pass
    with open('kern_log.txt', 'w') as fh:
        fh.write('\n'.join(logl))
    double = '\n'.join(kl)
    with open('double_kerns.oti', 'w') as fh:
        fh.write(double)
    # ~ for ke in kl:
        # ~ log_lib.debug(ke)
    log_lib.debug('liczba podwójnych niezgodnych kernów w pliku OTI: %d' % len(bad))
    log_lib.debug('liczba podwójnych kernów w pliku OTI: %d' % len(kl))
    log_lib.debug('liczba rozpoznanych kernów w pliku OTI: %d' % len(ki))
    return kl



# ------------------------------------------------------------------------------
di = '/1/mini/programowanie/0tematy/fonty/002_nowy_etap_z_poszerzonym_językiem_programowania_konfiguracji/03_py/lm_fea/03_towards_python'
afm_fn = 'lmr10.afm'
oti_fn = 'lmr10.oti'

# ~ di = '/1/mini/programowanie/0tematy/fonty/002_nowy_etap_z_poszerzonym_językiem_programowania_konfiguracji/50_out/2019_09_09_00_42/oti'
# ~ oti_fn = 'qagb.oti'



afm_path = os.path.join(di, afm_fn)
oti_path = os.path.join(di, oti_fn)

# ~ with open(afm_path, 'r') as fh:
    # ~ afm_str = fh.read()

with open(oti_path, 'r') as fh:
    oti_str = fh.read()

# ~ log_lib.debug(oti_str)

# ~ afm_kerns(afm_str)
oti_kerns(oti_str)



gly = read_oti_kerns_mt(oti_str)

# ~ log_lib.debug(gly.keys())
log_lib.debug(len(gly.keys()))

kpx_count = 0
for k in gly:
    if 'KPX' in gly[k]:
        kpx_count += len(gly[k]['KPX'])
# ~ log_lib.debug(gly['A'])
log_lib.debug(kpx_count)




json_kern = json_font_lib.kern_info(gly)

# ~ log_lib.debug(json_kern.keys())
log_lib.debug(len(json_kern.keys()))
# ~ log_lib.debug(json_kern['A'])


kern_count = 0
for k in json_kern:
    kern_count += len(json_kern[k])

log_lib.debug(kern_count)










def main(inp, template_name, output, q=True):
    global quiet
    quiet = q

    log_lib.debug(inp, template_name, output)
    iname = inp.strip()
    iname = re.sub(r'\.[^\.]+$', '.oti', iname)
    oname = output
    
    log_lib.info("OTI < " + iname)

    oti = ffdklib3.read_oti(iname)
    oti_fnt = oti['font']
    oti_gly = oti['glyphs']
    glyn_lst = oti['list']

    # prepare the name of the feature template file
    if template_name:
        template_name = template_name.strip()
        log_lib.info("TPL < %s" % template_name)
        template = read_template(template_name)
    # template is a list of strings
    # (possibly a single-string list or more then 300 strings)

    # ~ log_lib.debug(template)
    
    version = oti_fnt['VERSION']
    # ~ version = oti_fnt.keys()
    
    log_lib.debug(version)

    prefix = template.replace(template_patern, version)

    # ~ log_lib.debug(prefix)
    
    for k in oti_fnt:
        log_lib.debug('%s: %s' % (k, oti_fnt[k]))
    
    fea_data = prepare_fea_data(oti_fnt)
    
    log_lib.debug(fea_data)

    ki = prepare_kern_info(oti_gly)
    log_lib.debug(ki.keys())
    
    # count the number of kerns:
    kern_count = 0
    for k1 in ki:
        for k2 in k1:
            kern_count += 1
    log_lib.debug('There are %d kerns.' % kern_count)
    
    sd = prepare_size_data()
    for k in sd:
        log_lib.debug('%s: %s' % (k, sd[k]))

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
