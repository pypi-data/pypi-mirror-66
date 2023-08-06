#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
pfb_lib.py
Parse (disassemble), replace some parts and serialize (assemble) PFB file.

Marek Ryćko

start
16.01.2020 20:35:31
'''

# standard library:

import re
# for sys.exit:
import sys
# for translating float values to fractions:
from fractions import Fraction
# for calculating date string in a new pfb font:
from datetime import datetime

# Algotype:
import algotype.log_lib as log_lib

# ------------------------------------------------------------------------------
# general utilities:
# ------------------------------------------------------------------------------

'''
Translate to Python the following AWK function, programmed by B. Jackowski:

function rational(x,nlimit,dlimit, p0,q0,p1,q1,p2,q2,s,ds) {
  # a simplified version of the code kindly sent us by Berthold K. P. Horn
  if (x == 0.0) return "0 1" # if (x == 0.0) return "0/1"
  if (x < 0.0) return "-" rational(-x, nlimit, dlimit)
  # if (int(x) > nlimit) return round(x) # unlikely (in Type 1 fonts)
  p0=0; q0=1; p1=1; q1=0; s=x;
  while (1) {
    # in general, it is advisable to avoid crossing limits;
    # here, it is perhaps a bit of pedantry:
    if ( int(s)!=0 &&\
      ((p1 > (nlimit-p0)/int(s)) || (q1 > (dlimit-q0)/int(s))) )
      {p2=p1; q2=q1; break}
    p2=p0+int(s)*p1; q2=q0+int(s)*q1;
#   printf("%ld %ld %ld %ld %ld %ld %lg\n", p0, q0, p1, q1, p2, q2, s)
    if (p2/q2==x) break
    ds=s-int(s)
    if (ds == 0.0) break
    p0=p1; q0=q1; p1=p2; q1=q2; s=1/ds
  }
  # q2 != 0
  return p2 " " q2 # the answer is p2/q2
}
'''

def rational(x, nlimit, dlimit):
    '''
    Convert a float number x
    to a fraction of two integer numbers, returned as a tuple of int-s
    
    This function is to be called like this:
    rational(x, 32767, 32767)
    
    This is a simplified version of the code kindly sent
    to the GUST font e-foundry
    by Berthold K. P. Horn.
    '''
    if x == 0.0:
        # if x == 0.0: return "0/1"
        return (0, 1)
    elif x < 0.0:
        # for the strictly negative number
        # calculate the fraction for the absolute value
        # and then return it, converting nominator to negative
        n, d = rational(-x, nlimit, dlimit)
        return (-n, d)

    # if (int(x) > nlimit) return round(x) # unlikely (in Type 1 fonts)

    p0 = 0
    q0 = 1
    p1 = 1
    q1 = 0
    s = x
    
    while True:
        # in general, it is advisable to avoid crossing limits;
        # here, it is perhaps a bit of pedantry:
        if int(s) != 0 and \
                ((p1 > (nlimit - p0) / int(s)) or \
                (q1 > (dlimit - q0) / int(s))):
            p2 = p1
            q2 = q1
            break
        
        p2 = p0 + int(s) * p1
        q2 = q0 + int(s) * q1
        
        # log_lib.debug('%d %d %d %d %d %d %f' % (p0, q0, p1, q1, p2, q2, s))
        
        if p2 / q2 == x:
            # the result is exact and ready:
            break
            
        # if s is in fact integer -- we are done
        ds = s - int(s)
        if ds == 0.0:
            break
            
        # prepare the state for the next round of the loop
        p0 = p1
        q0 = q1
        p1 = p2
        q1 = q2
        s = 1 / ds
    
    # loop is finished:    
    # q2 != 0
    
    # the answer is p2/q2
    res = (p2, q2)
    return res

# ------------------------------------------------------------------------------
# parsing:
# ------------------------------------------------------------------------------

def pfd_to_struct(pfd_string):
    '''
    Parse pfd file (disassembled pfb file) to a structure as defined below.
    
    Read a pfd file and split it into substrings.
    Some substrings are to remain unchanged
    and some other are to be further parsed.
    '''
    # split to lines:
    lines = pfd_string.splitlines()

    i = 0



    
    # read initial comments up to the %%EndComments line
    
    comments = []
    pattern = r'^\s*%%EndComments\s*$'
    mo = re.search(pattern, lines[i])
    while not mo:
        comments.append(lines[i])
        i += 1
        mo = re.search(pattern, lines[i])
        
    # ~ log_lib.debug(comments[-5:])
    

    # read preamble up to the /CharStrings dict begin line
    # 2 index /CharStrings 822 dict dup begin

    preamble = []
    pattern = r'index \/CharStrings ([0-9]+) dict dup begin$'
    mo = re.search(pattern, lines[i])
    while not mo:
        preamble.append(lines[i])
        i += 1
        mo = re.search(pattern, lines[i])
        
    # ~ log_lib.debug(preamble[-5:])
        
    # we are at the line of the shape:
    # 2 index /CharStrings 822 dict dup begin
    # ~ log_lib.debug(lines[i])
    
    # save the number of elements:
    no_of_glyphs = int(mo.group(1))
    # ~ log_lib.debug(no_of_glyphs)
    
    # append the CharStrings header line also to the preamble
    # and move forward:
    preamble.append(lines[i])
    i += 1
    
    # we are at the beginning of first glyph info
    
    # read the glyphs info, pack into a structure and put into a list:
    glyphs = []
    for glyph_index in range(no_of_glyphs):
        # read a single glyph info and save partially parsed structure
        
        # read a glyph name line:
        pattern = r'^\/([a-zA-Z.0-9\_]+) {$'
        mo = re.match(pattern, lines[i])
        # save only a logical info:
        if mo:
            glyph_name = mo.group(1)
        else:
            log_lib.critical('wrong glyph name line:', lines[i])
        
        # ~ log_lib.debug('name line', lines[i])
        i += 1
        
        
        # ----------------------------------------------------------------------
        # new style of reading hsbw:
        
        i_saved = i
        
        # read the lines until the hsbw line
        # with possibly some div-s denoting fractional parameters
        
        # pattern for the hsbw line (just antything followed by “ hsbw”):
        pattern = r'^.*\shsbw$'
        mo = re.match(pattern, lines[i])
        # collect hsb group paramters (as line strings):
        hsbw_group = []
        while not mo:
            hsbw_group.append(lines[i])
            i += 1
            mo = re.match(pattern, lines[i])
            
        # the last read line is the hsbw line
        # append it to the hsbw group
        hsbw_group.append(lines[i])
        i += 1

        # join the hsbw group with spaces
        # and split to lexical units:
        
        hsbw_string = (' '.join(hsbw_group)).strip()
        hsbw_prog = hsbw_string.split()
        if len(hsbw_prog) != 3:
            # ~ log_lib.debug(hsbw_prog)
            pass
            
        # execute a small PostScript interpreter on a hsb_prog
        
        # execution stack of the interpreter:
        hsbw_stack = []
        
        for expr in hsbw_prog:
            # execute an expression expr on a stack hsbw_stack
            if expr == 'div':
                # replace operands on stack with a pair (nominator, denominator)
                pair = [hsbw_stack[-2], hsbw_stack[-1]]
                hsbw_stack[-2:] = []
                hsbw_stack.append(pair)
            elif  expr == 'hsbw':
                # nothing to do; operands are ready
                pass
            else:
                # should be a string representing an integer number
                hsbw_stack.append(int(expr))
            
        if len(hsbw_prog) != 3:
            # ~ log_lib.debug(' ' * 15, hsbw_stack)
            pass
            
        # ~ log_lib.debug(' ' * 3, hsbw_stack)
        # make sure the hsbw_stack is 2-element long
        assert(len(hsbw_stack) == 2)
        
        # the (possibly complex) hsbw parameter is:
        hsbw_param = hsbw_stack
        
        i = i_saved
        # ----------------------------------------------------------------------
        
        
        
        
        
        
        # optionally read a div line of the form:
        # 83374 1024 div
        
        # read a div line:
        pattern = r'^\s*([\+\-]?[0-9]+)\s+([\+\-]?[0-9]+)\s+div$'
        mo = re.match(pattern, lines[i])
        # save only a logical info:
        if mo:
            div_par = [int(mo.group(1)), int(mo.group(2))]
            # ~ log_lib.debug('div pair', div_par)
            i += 1

            # read a hsbw line with a single parameter:
            pattern = r'^\s*([\+\-]?[0-9]+)\s+hsbw$'
            mo = re.match(pattern, lines[i])
            # save only a logical info:
            if mo:
                hsbw_par = [int(mo.group(1))]
            else:
                log_lib.critical('does not match', lines[i])
            
            # ~ log_lib.debug('hsbw par', hsbw_par)

            i += 1

        else:
            div_par = None
        
            # read a hsbw double parameter line:
            pattern = r'^\s*([\+\-]?[0-9]+)\s+([\+\-]?[0-9]+)\s+hsbw$'
            mo = re.match(pattern, lines[i])
            # save only a logical info:
            if mo:
                hsbw_par = [int(mo.group(1)), int(mo.group(2))]
            else:
                log_lib.critical(lines[i])

            i += 1
                
        glyph_tail = []
        pattern = r'^\s*\}\s+ND\s*$'
        mo = re.match(pattern, lines[i])
        while not mo:
            glyph_tail.append(lines[i])
            i += 1
            mo = re.search(pattern, lines[i])

        # append also the closing glyph line:
        glyph_tail.append(lines[i])
        i += 1
        
        glyph_info = {
            'name': glyph_name,
            # pair of div parameters or None:
            'div_par': div_par,
            # a list of one or two hsbw parameters (always):
            'hsbw_par': hsbw_par,
            # new style hsbw parameter:
            'hsbw_param': hsbw_param,
            # a list of lines of the rest of glyph
            'tail': glyph_tail,
        }
        
        glyphs.append(glyph_info)
        
    # we are or should be just after the glyphs description
    
    

    postamble = lines[i:]
    # ~ log_lib.debug(postamble[0])
    
    res = {
        'comments': comments,
        'preamble': preamble,
        'postamble': postamble,
        'glyphs': glyphs,
    }
    
    return res
    
# ------------------------------------------------------------------------------
# conversion of the initial comments:
# ------------------------------------------------------------------------------

    
'''
replace comments of the shape (as generated by FontForge):

%!PS-AdobeFont-1.0: LMRomanDemi10-Regular 2.004
%%Title: LMRomanDemi10-Regular
%Version: 2.004
%%CreationDate: Tue Jan 21 12:36:41 2020
%%Creator: Marek Ryćko,,,
%Copyright: Copyright 2003--2009 by B. Jackowski and J.M. Nowacki (on
%Copyright:  behalf of TeX USERS GROUPS).
% 2020-1-21: Created with FontForge (http://fontforge.org)
% Generated by FontForge 20170924 (http://fontforge.sf.net/)
%%EndComments

to comments of the shape (as used to be in the distribution):

%!PS-AdobeFont-1.0: LMRomanDemi10-Regular 2.004
%%CreationDate: 7th October 2009
% Generated by MetaType1 (a MetaPost-based engine)
% Copyright 2003--2009 by B. Jackowski and J.M. Nowacki (on behalf of TeX USERS GROUPS).
% Supported by CSTUG, DANTE eV, GUST, GUTenberg, NTG, and TUG.
% METATYPE1/Type 1 version by B. Jackowski & J. M. Nowacki
% from GUST (http://www.gust.org.pl).
% This work is released under the GUST Font License.
% For the most recent version of this license see
% This work has the LPPL maintenance status `maintained'.
% The Current Maintainer of this work is Bogus\l{}aw Jackowski and Janusz M. Nowacki.
% This work consists of the files listed in the MANIFEST-Latin-Modern.txt file.
% ADL: 806 194 0
%%EndComments

'''


def initial_comment_lines(json_font):
    '''
    Create the list of initial comment lines.
    
    ...up to but not including the %%EndComments line
    '''
    
    now = datetime.now()
    now_string = now.strftime('%B %d, %Y, %H:%M:%S')
    version = json_font['par']['attr']['version']
    engine = 'Algotype'
    generated_by = f'{engine} (a MetaPost-based engine)'
    type_one_version_by = 'B. Jackowski & J. M. Nowacki'
    maintainer = 'Bogus\l{}aw Jackowski and Janusz M. Nowacki.'
    originally_generated_by = 'FontForge (http://fontforge.org)'
    ascent = int(json_font['par']['attr']['ascent'])
    descent = int(json_font['par']['attr']['descent'])
    linegap = int(json_font['par']['attr']['hhea_linegap'])
    
    initial_comments_lines = [
        f"%!PS-AdobeFont-1.0: {json_font['par']['attr']['fontname']} {version}",
        f"%%CreationDate: {now_string}",
        f"% Generated by {generated_by}",
        f"% Originally generated by {originally_generated_by}",
        f"% {json_font['par']['attr']['copyright']}",
        f"% Supported by CSTUG, DANTE eV, GUST, GUTenberg, NTG, and TUG.",
        f"% {engine}/Type 1 version by {type_one_version_by}",
        f"% from GUST (http://www.gust.org.pl).",
        f"% This work is released under the GUST Font License.",
        f"% For the most recent version of this license see",
        f"% This work has the LPPL maintenance status `maintained'.",
        f"% The Current Maintainer of this work is {maintainer}",
        f"% This work consists of the files listed in the MANIFEST-Latin-Modern.txt file.",
        f"% ADL: {ascent} {descent} {linegap}",
        # ~ f"%%EndComments",
        ]
    # ~ initial_comments_string = '\n'.join(initial_comments_fstrings)
    # ~ res = initial_comments_string.splitlines()

    res = initial_comments_lines
    return res
















    
# ------------------------------------------------------------------------------
# conversion of glyphs data (within the structure):
# ------------------------------------------------------------------------------

    
    
def pfd_struct_translate(pfd_struct, json_font):
    '''
    Translate parameters of hsbw in glyphs using values from json_font.
    
    The structure the pfd_struct dictionary:
    
    {
        'preamble': preamble,
        'postamble': postamble,
        'glyphs': glyphs,
    }
    '''
    # change the initial comments:
    comments_new = initial_comment_lines(json_font)
    
    # chagne some parts of glyphs:
    
    glyphs = pfd_struct['glyphs']
    new_glyphs = []
    
    unknown_names = []
    float_offsets = []
    float_widths = []
    
    for glyph in glyphs:
        # create a new glyph with replaced glyph['hsbw_param']:
        new_glyph = {}
        # name and tail remain unchanged:
        name = glyph['name']
        new_glyph['name'] = name
        new_glyph['tail'] = glyph['tail']
        # calculate new hsbw parameters:

        # we take values from json_font for real names, not “.notdef”
        # or other not found...
        # ~ if name != '.notdef':
        if name in json_font['glyphs']:
            # calculating new hsbw paramters:
            
            # the first parameter is the character offset:
            bbox = json_font['glyphs'][name]['meta']['HiResBoundingBox']
            # bbox is probably a 4-element list of integers/floats
            # here we are interested only in the first value, llx:
            llx = bbox[0]
            # llx is integer or float
            if isinstance(llx, float):
                float_offsets.append(llx)
            hsbw_0 = number_to_possibly_fraction(llx)
                
            # the second paramter is the character box width (with offsets):
            wd = json_font['glyphs'][name]['metrics']['width']
            if isinstance(wd, float):
                float_widths.append(wd)

            hsbw_1 = number_to_possibly_fraction(wd)
            
        elif name == '.notdef':
            # new style hsbw parameter:
            # just repeat the parameters from the original pfbL
            [hsbw_0, hsbw_1] = glyph['hsbw_param']
            # ~ hsbw_0 = 0
            # ~ hsbw_1 = 500
        else:
            # ~ log_lib.debug(f'glyph not found in OTI: {name}')
            log_lib.debug(f'glyph not found in OTI: {name}')
            unknown_names.append(name)
            hsbw_0 = 0
            hsbw_1 = 0
            
        new_glyph['hsbw_param'] = [hsbw_0, hsbw_1]
        new_glyphs.append(new_glyph)
        
    if len(unknown_names) > 0:
        log_lib.debug(f'number of PFB glyph names not found in OTI: {len(unknown_names)}')
    for nam in unknown_names:
        # ~ log_lib.debug(nam)
        pass
    log_lib.debug('number of float offsets: %d' % len(float_offsets))
    for f in float_offsets:
        log_lib.debug(f"    float offset: {f}")
        pass
    log_lib.debug('number of float widths: %d' % len(float_widths))
    for f in float_widths:
        log_lib.debug(f"    float width: {f}")
        pass

    res = {
        'comments': comments_new,
        'preamble': pfd_struct['preamble'],
        'postamble': pfd_struct['postamble'],
        'glyphs': new_glyphs,
    }
    
    return res


def number_to_possibly_fraction(n):
    '''
    Convert n to a pair numerator, denominator if it is a float.
    '''
    if isinstance(n, int):
        # result is just an integer number:
        res = n
    else:
        # n must be a float
        if 0:
            # the Python way:
            fraction = Fraction(n)
            pair = [fraction.numerator, fraction.denominator]
        else:
            # the rational function from Metatype1 way:
            nlimit = 32767
            dlimit = 32767
            pair = rational(n, nlimit, dlimit)
            
        # ~ log_lib.debug('%f --> %s' % (n, str(pair)))
        res = pair
    return res



# ------------------------------------------------------------------------------
# serialization of the structure to lines and to a string:
# ------------------------------------------------------------------------------


def pfd_struct_to_lines(pfd_struct):
    '''
    Serialize a pfd (disassembled pfb) structure to a list of lines.
    
    The structure is a dictionary:
    
    {
        'preamble': preamble,
        'postamble': postamble,
        'glyphs': glyphs,
    }
    '''
    # string list:
    sl = []
    sl.extend(pfd_struct['comments'])
    sl.extend(pfd_struct['preamble'])
    sl.extend(pfd_glyphs_to_lines(pfd_struct['glyphs']))
    sl.extend(pfd_struct['postamble'])

    return sl
    

    
    
def pfd_glyphs_to_lines(glyphs):
    '''
    serialize a list of glyphs to lines
    '''
    
    sl = []
    for glyph in glyphs:
        # serialize the glyph and append to the result
        
        # glyph string list:
        gsl = []
        # name line:
        gsl.append('/%s {' % glyph['name'])
        
        # hsbw section:
        
        gsl.extend(hsbw_to_lines(glyph['hsbw_param']))
            
        gsl.extend(glyph['tail'])
    
        # gsl is the glyph’s string list
        sl.extend(gsl)

    return sl
    
def hsbw_to_lines(hsbw_param):
    '''
    Serialize the hsbw_param as a series of lines.
    
    The param is a 2-element list. Each element may be one of:
        -- integer
        -- pair of integers (nominator, denominator)
        
    The result may be one or more lines, but in all cases
    a list of lines.
    '''
    # string list, probably to be further put in one line
    sl = []
    
    for p in hsbw_param:
        # p is a single parameter, one of two
        if isinstance(p, int):
            # just an integer value:
            sl.append(str(p))
        else:
            # should be a pair of integers:
            sl.append(str(p[0]))
            sl.append(str(p[1]))
            sl.append('div')
    # complete the string list with the main function name:
    sl.append('hsbw')
    
    # ~ res = ' ' * 4 + ' '.join(sl)
    res = '\t' + ' '.join(sl)
    return [res]
    
# ------------------------------------------------------------------------------
# summary: translation of disassembled pfb string using json_font structure:
# ------------------------------------------------------------------------------

def pfd_convert(pfd_string, json_font):
    
    # parse pfd string and convert to a structure:
    pfd_struct = pfd_to_struct(pfd_string)
    # translate/convert pdf_struct, using json_font:
    pfd_struct_new = pfd_struct_translate(pfd_struct, json_font)
    pfd_lines = pfd_struct_to_lines(pfd_struct_new)
    pfd_string_new = '\n'.join(pfd_lines)
    return pfd_string_new



if __name__ == '__main__':
    import os
    import json
    
    di = 'pfb_asm'
    fbb = 'lmb10'
    #fb = 'lmb10.distrib'
    fb = 'lmb10.goadb_04'
    bfn = fb + os.extsep + 'pfb'
    # disassembled file name:
    dfn = fb + os.extsep + 'pfd'
    # working log filename:
    lfn = fb + os.extsep + 'log'

    # json font filename:
    json_font_fn = fbb + '_font' + os.extsep + 'json'

    dpath = os.path.join(di, dfn)
    
    json_font_path = os.path.join(di, json_font_fn)

    
    with open(dpath, 'r') as fh:
        pfd_string = fh.read()
        
    # read input json font:

    with open(json_font_path, 'r') as fh:
        json_font_string = fh.read()

    json_font = json.loads(json_font_string)
    
    
    
    ini_com = initial_comment_lines(json_font)
    for l in ini_com:
        log_lib.debug(l)
    
    

    if 1:
        pfd_string_new = pfd_convert(pfd_string, json_font)
    else:

        pfd_struct = pfd_to_struct(pfd_string)
        
        # translate pdf_struct:
        fool = pfd_struct_translate(pfd_struct, json_font)
        
        pfd_lines = pfd_struct_to_lines(pfd_struct)
        pfd_string = '\n'.join(pfd_lines)

    # ~ for l in pfd_lines:
        # ~ log_lib.debug(l)
        # ~ pass
    
    with open(os.path.join(di, fb + os.extsep + 'generated.pfd'), 'w') as fh:
        fh.write(pfd_string_new)

    
    # ~ log_lib.debug(pfd_struct['postamble'])