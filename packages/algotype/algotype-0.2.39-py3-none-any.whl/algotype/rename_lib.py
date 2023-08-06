#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
rename_lib.py
parser of renaming definition files
and serving the json structures defining the renaming
    of otf fonts, pfb fonts and encodings

Marek Ryćko

start as a copy of afm_parse
19.04.2020 18:16:34
completed:
...
'''

# standard library:

import re
# for sys.exit:
import sys

# Algotype:
if __name__ == '__main__':
    import log_lib
    log_lib.start_log()
else:
    import algotype.log_lib as log_lib


# ------------------------------------------------------------------------------
# general utilities:
# ------------------------------------------------------------------------------

# none

# ------------------------------------------------------------------------------
# parsing:
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# parsing utilities (possibly furtner to some library):
# ------------------------------------------------------------------------------

def to_significant_lines(s):
    '''
    Split a multiline string s to lines, leaving only significant ones.
    
    Filter out -- empty, whitespace and comment lines.
    '''
    sl = s.splitlines()
    # remove leading and trailing whitespace:
    sl = [e.strip() for e in sl]
    # remove empty (previously whitespace only) lines:
    sl = [e for e in sl if e]
    # remove lines commented out:
    sl = [e for e in sl if not (e.startswith('#') or e.startswith('%'))]
    return sl



# ------------------------------------------------------------------------------
# renaming otf (and sfd) names:
# ------------------------------------------------------------------------------

def otf_names_to_line_struct(otf_names_string):
    '''
    Parse the string (file) defining renaming otf files.
    
    19.04.2020 18:42:05
    '''
    sl = to_significant_lines(otf_names_string)
    
    # sl is a list of strings
    res = []
    for l in sl:
        mo = re.match(r'^(.+)\s+\-\>\s+(.+)$', l)
        if mo:
            line_struct = {'source': mo.group(1), 'target': mo.group(2)}
            res.append(line_struct)
        else:
            log_lib.error(f"OTF renaming; wrong line structure: {l}")
            
    # parse the line
    
    return res
    
def otf_line_struct_to_dict(otf_line_struct):
    '''
    Convert otf renaming definition from list of line structs to a dictionary.
    
    19.04.2020 22:59:47
    '''
    
    d = {}
    ok = True
    for l in otf_line_struct:
        # ~ source, target = l
        if l['source'] in d:
            ok = False
            m = f"repeated source name; line: {l['source']} -> {l['target']}"
            log_lib.error(m)
        else:
            d[l['source']] = l['target']
            
    return d
            
def otf_rename_str_to_dict(otf_def_str):
    otf_def_list = otf_names_to_line_struct(otf_def_str)
    d = otf_line_struct_to_dict(otf_def_list)
    return d
    
# ------------------------------------------------------------------------------
# renaming in type1/pfb generation of tfm and enc names:
# ------------------------------------------------------------------------------

'''
definition file/string structure:

<metapost font base name (fb)>
followed by a series of triples:
<tfm basename> <encoding name.enc> {<internal encoding name>}

sample:

lmb10
cs-lmb10 lm-cs.enc {enclmcs}
ec-lmb10 lm-ec.enc {enclmec}
l7x-lmb10 lm-l7x.enc {enclml7x}
qx-lmb10 lm-qx.enc {enclmqx}
rm-lmb10 lm-rm.enc {enclmrm}
t5-lmb10 lm-t5.enc {enclmt5}
texnansi-lmb10 lm-texnansi.enc {enclmtexnansi}
ts1-lmb10 lm-ts1.enc {enclmts1}

lmbo10
cs-lmbo10 lm-cs.enc {enclmcs}
ec-lmbo10 lm-ec.enc {enclmec}
l7x-lmbo10 lm-l7x.enc {enclml7x}
qx-lmbo10 lm-qx.enc {enclmqx}
rm-lmbo10 lm-rm.enc {enclmrm}
t5-lmbo10 lm-t5.enc {enclmt5}
texnansi-lmbo10 lm-texnansi.enc {enclmtexnansi}
ts1-lmbo10 lm-ts1.enc {enclmts1}

plus some empty and comment lines

'''

def pfb_def_to_line_struct(pfb_def_string):
    '''
    Parse the string (file) defining pfb_def.
    
    20.04.2020 14:23:47
    '''
    sl = to_significant_lines(pfb_def_string)
    
    # sl is a list of strings
    
    # collect a dictionary of structures (triples so far)
    res = {}
    last_fb = None
    for l in sl:
        # parse the line

        # there are two possible forms of lines:
        # 1. a single base font name, like qtmr
        # 2. a triple of: tfm basename, enc file name, {enc internal}
        
        # split the line on (sequences of) spaces:
        fields = l.split()
        # ~ print(fields)
        if len(fields) == 1:
            # this is (supposedly) a font basename:
            fb = fields[0]
            if fb in res:
                # repeated font name:
                log_lib.warning(f"PFB structures renaming; repeated font name: {fb}")
                m = f"PFB structures renaming; adding the group following: {fb} " + \
                    f"to the previous of the same base font filename"
                log_lib.warning(m)
                last_fb = fb
            else:
                # a fresh new group of data
                last_fb = fb
                # start collecting a dictionry representing a list of triples:
                res[fb] = {}
                # not skipping the following group
                skipping = False
                
            # ~ print(fb)
        elif len(fields) == 3:
            # this is an element for the last fb
            first, second, third = fields
            
            # check the correctness of the second field:
            mo = re.match(r'^(.+)\.enc$', second)
            if mo:
                # second becomes the second field with '.enc' removed:
                second = mo.group(1)
            else:
                log_lib.error(f"PFB structures renaming; wrong structure of the second field: {second}")

            # check the correctness of the third field:
            mo = re.match(r'^\{(.+)\}$', third)
            if mo:
                third = mo.group(1)
            else:
                log_lib.error(f"PFB structures renaming; wrong structure of the third field: {third}")
            
            # verify the internal construction of the third field
            # wrt. second field:
            pattern = r'(\-)+'
            repl = ''
            second_core = re.sub(pattern, repl, second)
            maybe_third = 'enc' + second_core
            
            if third != maybe_third:
                log_lib.error(f"PFB structures renaming; wrong internal structure of the third field")
                log_lib.error(f"is: {third}, should be: {maybe_third}")
            
            # ~ log_lib.info(f"is: {third}, should be: {maybe_third}")
            
            if fb is None:
                m = f"no base font filename preceding triple: " + \
                    "{first} {second} {third}"
                log_lib.error(m)
            else:
                if first in res[fb]:
                    m = f"repeated base tfm name {first} in the group {fb}"
                    log_lib.error(m)
                else:
                    res[fb][first] = [second, third]
            
        else:
            # wrong number of fields:
            log_lib.error(f"PFB structures renaming; wrong line structure: {l}")
            
    
    return res



# ------------------------------------------------------------------------------
# mp/enc relation:
# ------------------------------------------------------------------------------

def enc_mp_def_to_line_struct(enc_mp_def_str):
    '''
    Create a relation between enc names and mp (mp-encoding) names.
    
    Translate mp_enc string to a list of pairs:
    
    the input looks like this:
    
    # LM PS <- MP:

    lm-cs.enc <- e-cs.mp
    lm-cssc.enc <- e-cscsc.mp
    lm-cstt.enc <- e-cstt.mp
    lm-ec.enc <- e-ec.mp
    lm-l7x.enc <- e-l7x.mp
    lm-qx.enc <- e-qx.mp
    lm-qxsc.enc <- e-qxcsc.mp
    lm-qxtt.enc <- e-qxtt.mp
    lm-rm.enc <- e-rm.mp
    lm-rmsc.enc <- e-rmcsc.mp
    lm-rmtt.enc <- e-rmtt.mp
    lm-t5.enc <- e-t5.mp
    lm-texnansi.enc <- e-yy.mp
    lm-ts1.enc <- e-ts1.mp

    # TG PS <- MP:

    q-cs-sc.enc <- e-cscs.mp
    q-cs.enc <- e-cs.mp
    q-csm-sc.enc <- e-csttsc.mp
    q-csm.enc <- e-cstt.mp
    q-cszc.enc <- e-cs.mp
    q-ec-sc.enc <- e-ecsc.mp
    q-ec.enc <- e-ec.mp
    q-l7x-sc.enc <- e-l7xsc.mp
    q-l7x.enc <- e-l7x.mp
    q-l7xzc.enc <- e-l7x.mp
    q-qx-sc.enc <- e-qxsc.mp
    q-qx.enc <- e-qx.mp
    q-qxm-sc.enc <- e-qxttsc.mp
    q-qxm.enc <- e-qxtt.mp
    q-qxzc.enc <- e-qx.mp
    q-rm-sc.enc <- e-rmsc.mp
    q-rm.enc <- e-rm.mp
    q-rmm-sc.enc <- e-rmttsc.mp
    q-rmm.enc <- e-rmtt.mp
    q-rmzc.enc <- e-rm.mp
    q-t5-sc.enc <- e-t5sc.mp
    q-t5.enc <- e-t5sc.mp
    q-texnansi-sc.enc <- e-yysc.mp
    q-texnansi.enc <- e-yy.mp
    q-texnansizc.enc <- e-yy.mp
    q-ts1.enc <- e-ts1.mp

    '''

    sl = to_significant_lines(enc_mp_def_str)
    
    # sl is a list of strings
    
    # collect a dictionary of structures (triples so far)
    # ~ return sl

    lines = []
    for s in sl:
        mo = re.match(r'^\s*(.+)\.enc\s+\<\-\s+(.+)\.mp\s*$', s)
        if mo:
            # the line has a correct construction
            enc = mo.group(1)
            mp = mo.group(2)
            dic = {'enc': enc, 'mp': mp}
            
        else:
            log_lib.error(f"enc/mp relation: wrong structure of the line: {s}")
            dic = {'enc': '', 'mp': ''}
        lines.append(dic)
        
    # just for understanding; analysing uniqueness:
    
    enc_to_mp = {}
    mp_to_enc = {}
    for d in lines:
        enc = d['enc']
        mp = d['mp']
        # list of mp-s for enc
        if enc in enc_to_mp:
            enc_to_mp[enc].append(mp)
        else:
            enc_to_mp[enc] = [mp]
        # list of enc-s for mp:
        if mp in mp_to_enc:
            mp_to_enc[mp].append(enc)
        else:
            mp_to_enc[mp] = [enc]
    # the two dictionaries are ready
    # test the uniqueness:
    
    ok = True
    for enc in enc_to_mp:
        if len(enc_to_mp[enc]) > 1:
            ok = False
            log_lib.error(f"enc/mp relation: ambigious relation from enc to mp:")
            log_lib.error(f"    {repr(enc)}")
            break
    # ok or not ok
            
    if 0:
        # just tests:
        for enc in enc_to_mp:
            # ~ if len(enc_to_mp[enc]) > 1:
            if 0:
            # ~ if 1:
                print(f"enc_to_mp[{repr(enc)}] = {repr(enc_to_mp[enc])}")
        for mp in mp_to_enc:
            # ~ if len(mp_to_enc[mp]) > 1:
            # ~ if len(mp_to_enc[mp]) == 1:
            if 0:
                print(f"mp_to_enc[{repr(mp)}] = {repr(mp_to_enc[mp])}")
            
    # so enc_to_mp is a function; can be represented as a mapping
    # if we know the encoding name, we know the metapost file name to be used
    
    # values of the mapping will no more be lists:
    for enc in enc_to_mp:
        enc_to_mp[enc] = enc_to_mp[enc][0]
    
        

    return enc_to_mp
    
def main(conf):
    '''
    Read renaming files and parse them into json structures.

    The definitions in config may look like this:
    otf_renaming_file = $renaming_dir change_otf_names.txt
    pfb_renaming_file = $renaming_dir change_pfb_names.txt
    enc_mp_relation_file = $renaming_dir enc_ps_mp_names.txt

    '''
    
    otf_def_path = conf['otf_renaming_file']
    pfb_def_path = conf['pfb_renaming_file']
    enc_mp_def_path = conf['enc_mp_relation_file']
    
    # --------------------------------------------------------------------------
    # otf renaming definition:
    
    with open(otf_def_path, 'r') as fh:
        otf_def_str = fh.read()
        
    otf_def_list = otf_names_to_line_struct(otf_def_str)
    otf_def_dict = otf_line_struct_to_dict(otf_def_list)
   
    # --------------------------------------------------------------------------
    # pfb (tfm, enc) definition:

    with open(pfb_def_path, 'r') as fh:
        pfb_def_str = fh.read()
        
    pfb_def_struct = pfb_def_to_line_struct(pfb_def_str)
    
    # --------------------------------------------------------------------------
    # enc mp relation definition:

    with open(enc_mp_def_path, 'r') as fh:
        enc_mp_def_str = fh.read()
        
    enc_mp_def_struct = enc_mp_def_to_line_struct(enc_mp_def_str)
    
    # --------------------------------------------------------------------------
    res = {
        'otf': otf_def_dict,
        'pfb': pfb_def_struct,
        'enc_mp': enc_mp_def_struct,
    }

    return res



if __name__ == '__main__':
    import os
    import json
    
    rdi = '/1/mini/programowanie/0tematy/fonty/007_towards_more_functionality/03_py/distr/inp/renaming'
    
    # --------------------------------------------------------------------------
    # otf renaming definition:
    otf_def_name = 'change_otf_names.txt'
    otf_def_path = os.path.join(rdi, otf_def_name)
    
    with open(otf_def_path, 'r') as fh:
        otf_def_str = fh.read()
        
    otf_def_list = otf_names_to_line_struct(otf_def_str)
    otf_def_dict = otf_line_struct_to_dict(otf_def_list)
    otf_def_len = len(otf_def_dict)
    otf_json_str = json.dumps(otf_def_dict, indent=4, ensure_ascii=False)
    # ~ print(otf_json_str)
    # ~ print(otf_def_len)
    
    # --------------------------------------------------------------------------
    # pfb (tfm, enc) definition:

    pfb_def_name = 'change_pfb_names.txt'
    pfb_def_path = os.path.join(rdi, pfb_def_name)
    
    with open(pfb_def_path, 'r') as fh:
        pfb_def_str = fh.read()
        
    stru = pfb_def_to_line_struct(pfb_def_str)
    
    stru_str = json.dumps(stru, indent=4, ensure_ascii=False)
    # ~ print(stru_str)
    print(len(stru))
    
    # --------------------------------------------------------------------------
    # enc mp relation definition:

    enc_mp_def_name = 'enc_ps_mp_names.txt'
    enc_mp_def_path = os.path.join(rdi, enc_mp_def_name)
    
    with open(enc_mp_def_path, 'r') as fh:
        enc_mp_def_str = fh.read()
        
    stru = enc_mp_def_to_line_struct(enc_mp_def_str)
    
    stru_str = json.dumps(stru, indent=4, ensure_ascii=False)
    print(stru_str)
    print(len(stru))
    
    
    
    # ~ otf_def_dict = otf_line_struct_to_dict(otf_def_list)
    # ~ otf_def_len = len(otf_def_dict)
    # ~ otf_json_str = json.dumps(otf_def_dict, indent=4, ensure_ascii=False)
    # ~ print(otf_json_str)
    # ~ print(otf_def_len)
    
    
    
    