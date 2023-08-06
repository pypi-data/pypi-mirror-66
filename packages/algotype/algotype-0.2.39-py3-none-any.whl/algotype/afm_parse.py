#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
afm_parse.py
parser of some class of AFM (Adobe Font Metric) files

Marek Ryćko

start as a copy of afm_lib
15.01.2020 15:43:49
completed:
16.01.2020 15:16:30
'''

# standard library:

import re
# for sys.exit:
import sys

# Algotype:
import algotype.log_lib as log_lib

# ------------------------------------------------------------------------------
# general utilities:
# ------------------------------------------------------------------------------

# none

# ------------------------------------------------------------------------------
# parsing:
# ------------------------------------------------------------------------------

def afm_string_to_line_structures(afm_strng):
    '''
    Translate the afm string to structures containing line numbers and strings.
    
    To keep trace of the input line numbers we split the input string
    (the contens of an AFM file) to stringns labelled with line numbers.
    The lines are returned in the form already left-stripped from the whitespace
    (we do not plan to point at the particural position of character
    within the line); there is no right-stripping as, formally, the
    trailing spaces are allowed as a part of a parameter string
    '''
    lines = afm_strng.splitlines()
    # lines is a list of strings
    res = []
    for i, l in enumerate(lines):
        # i is a line index, counted starting with 0
        mo = re.match(r'^\s*$', l)
        if mo:
            # this is an empty or whitespace line:
            # ~ log_lib.debug('empty line:', l)
            pass
        else:
            # i is the line index (counted from 0)
            # n is the line number (counted from 1)
            # l is the line string
            l = l.strip()
            # ~ if len(l) < 15:
                # ~ log_lib.debug('short line:', l)
            line_struct = {'i': i, 'n': i + 1, 'l': l}
            res.append(line_struct)
    return res
 
# a list of AFM keys with string values (string is then the only value):
string_keys = [
    'StartFontMetrics',
    'Comment',
    'FontName',
    'FullName',
    'FamilyName',
    'Weight',
    'Notice',
    'Version',
    'EncodingScheme',
    'CharacterSet',
    # ~ '',
]

# this is a dictionary of command parameter types
# (for the non-string parameters)
# the parameters will be checked and converted from strings accorgingly

# the specification is contradictory:
# StartKernData is with an integer parameter or without

# from:
# https://www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5004.AFM_Spec.pdf
# page 13, 14, 36

command_syntax = '''
StartFontMetrics number
EndFontMetrics

Comment string

FontName string
FullName string
FamilyName string
Weight string
FontBBox number number number number
Version string
Notice string
EncodingScheme string
MappingScheme integer
EscChar integer
CharacterSet string
Characters integer
IsBaseFont boolean
VVector number number
IsFixedV boolean
CapHeight number
XHeight number
Ascender number
Descender number

UnderlinePosition number
UnderlineThickness number
ItalicAngle number
CharWidth number number
IsFixedPitch boolean

StartCharMetrics integer
EndCharMetrics

# there is an error in AFM specification in definition of StartKernData
StartKernData
EndKernData

StartKernPairs integer
EndKernPairs

KPX name name number

# C line component commands:
C integer
WX number
N name
B number number number number
L name name

'''


command_types = {}

def command_syntax_to_command_types(command_syntax):
    '''
    Calculate a command types dictionary.

    Take a command syntax multiline string
    and transform it to a dictionary
        from command or subcommand names
        to lists of parameter types
    of the form:
    
    'StartFontMetrics': ['string'],
    'Comment': ['string'],
    'FontName': ['string'],
    'FullName': ['string'],
    'FamilyName': ['string'],
    'Weight': ['string'],
    'Notice': ['string'],
    'ItalicAngle': ['string'],
    'Version': ['string'],
    'EncodingScheme': ['string'],
    'CharacterSet': ['string'],
    
    '''
    lines = command_syntax.splitlines()
    # remove empty lines or comment lines
    lines_grammar = []
    for l in lines:
        if re.match(r'^\s*$', l) or re.match(r'^\s*\#.*$', l):
            pass
        else:
            lines_grammar.append(l)
    
    command_types = {}
    
    for lg in lines_grammar:
        cp = lg.split()
        command_types[cp[0]] = cp[1:]
            
    for lg in lines_grammar:
        # ~ log_lib.debug(lg)
        pass

    for ct in command_types:
        # ~ log_lib.debug(ct, command_types[ct])
        pass
        
    return command_types


def line_structure_to_command(ls):
    '''
    Translate a line structure as returned from afm_string_to_lines to a command.
    
    The input is a line-string along with a line number and index.
    
    The returned command is a structure with a command name and parameters.
    '''
    # take the line string from the stucture:
    line_string = ls['l']
    
    # first split on whitespace:
    elements = line_string.split(maxsplit=1)
    command = elements[0]
    if line_string.startswith('Comm'):
        # ~ log_lib.debug(command, command_types[command])
        pass
    # ~ if command in string_keys:
    ctype = command_types[command]
    if len(ctype) == 1 and ctype[0] == 'string':
        # the resulting command is a string-parameter command:
        p = elements[1] if len(elements) >= 2 else ''
        # ~ log_lib.debug(command, p)
        # command and parameter are ready; we create a 1-element parameter list:
        stru = {'c': command, 'p': [p]}
    else:
        # if the command parameter is not a string
        # then split the line even more
        if command == 'C':
            # this is a character metric command (with a bit complicated syntax)
            stru = char_metrics_line_to_command(ls)
            # ~ log_lib.debug(res)
        else:
            # this is a regular command with a sequence of parameters
            # store them, for now, as strings
            fine_elements = line_string.split()
            # fine_elements is a list of at least one element
            command = fine_elements[0]
            p = fine_elements[1:]
            stru = {'c': command, 'p': p}
            parsed = parse_parameters(stru)
            stru = parsed
            # ~ log_lib.debug(stru)
    # stru is a structure (dictionary) of command and unpaprsed parameter
    
    # the resulting dictionary is to contain all the stru
    # and other elements from ls (line number and index)
    stru.update(ls)
    # ...but without the original unparsed string:
    del stru['l']
            
    return stru
    
def char_metrics_line_to_command(ls):
    '''
    Translate a character metrics line structure to a command.
    '''
    # take the line string from the stucture:
    line_string = ls['l']
    
    # first split on semicolons, with possibly some whitespace around:
    # (the AFM specification is not clear about the whitespace)
    pattern = r'\s*;\s*'
    subexpression_strings = re.split(pattern, line_string)
    # discard the part after the last “;” if it is empty:
    if subexpression_strings[-1] == '':
        subexpression_strings = subexpression_strings[:-1]

    ligature_line = False
    
    # translate subexpressions to a structure of command name
    # and a list of parameter strings:
    sub = []
    for cs in subexpression_strings:
        elements = cs.split()
        # elements is a list of at least one element
        command = elements[0]
        if command == 'L':
            ligature_line = True
        p = elements[1:]
        cp = {'c': command, 'p': p}
        parsed = parse_parameters(cp)
        sub.append(parsed)
        
    res = {'c': 'C', 'p': sub}

    # ~ if ligature_line:
        # ~ log_lib.debug(res)

    return res
    
def parse_parameters(cp):
    '''
    Parse structure parameters checking them and converting strings to values.
    
    For a structure cp of a command and a list of string parameters
    test the number and types of parameters and convert them
    to Python/json values.
    
    cp = {'c': 'some-command', 'p': ['para', 'meter', ..., 'list']}
    '''
    command = cp['c']
    parameter_strings = cp['p']
    if command not in command_types:
        log_lib.critical('unknown AFM command %s' % command)

    types = command_types[command]
    # types is a list of types for the command command
        
    if len(types) != len(parameter_strings):
        log_lib.critical('wrong number of parameters %s' % str(parameter_strings))
    
    # number of paramteres and types are equal

    # the types can be:
    # number, ingeter, boolean, name
    # (string is eliminated; it has been parsed in a different way)
    
    parameter_values = []
    for i, s in enumerate(parameter_strings):
        # test and convert the i-ths parameter from s to v:
        
        expected_type = types[i]
        if expected_type == 'number':
            try:
                v = int(s)
            except:
                try:
                    v = float(s)
                except:
                    log_lib.critical('Expected number: %s' % s)
        elif expected_type == 'integer':
            try:
                v = int(s)
            except:
                log_lib.critical('Expected intenger: %s' % s)
        elif expected_type == 'boolean':
            if s in ('true', 'false'):
                v = True if s == 'true' else False
            else:
                log_lib.critical('Expected boolean: %s' % s)
        elif expected_type == 'name':
            v = s
            # nothing to verify here
            
        parameter_values.append(v)
        
    # ~ log_lib.debug('parameter values', parameter_values)
    
    res = {'c': command, 'p': parameter_values}
        
    return res
        
    

def line_structures_to_commands(lines):
    '''
    Translate all the line structures to commands with parameters.
    
    
    '''
    commands = []
    for ls in lines:
        c = line_structure_to_command(ls)
        if c is not None:
            commands.append(line_structure_to_command(ls))
        
    return commands
    
    

# ------------------------------------------------------------------------------
# list of parsed commands to the general afm logical structure
# with sections
# ------------------------------------------------------------------------------

def afm_commands_to_afm_structure(afm_commands):
    '''
    Translate a list of afm commands to a multi-section afm structure.
    
    Take a list of commands of the type:
    [
        {'c': 'some-command', 'p': list of paramters, ...},
        ...
    ]
    and translate it to an afm logical structure
    as used in afm_lib
    (this requires that comments are grupped just in two places)
    '''
    
    # collect data from the list of commands and put it
    # to sections of afm structure
    
    i = 0
    
    # font metrics version:
    assert(afm_commands[i]['c'] == 'StartFontMetrics')
    version = afm_commands[i]['p'][0]
    i += 1
    
    # initial comments:
    initial = []
    while afm_commands[i]['c'] == 'Comment':
        comment_string = ' '.join([afm_commands[i]['c'], afm_commands[i]['p'][0]])
        initial.append(comment_string)
        i += 1
    
    # header (general font parameters):
    header = {}
    while afm_commands[i]['c'] != 'Comment' and \
            afm_commands[i]['c'] != 'StartCharMetrics':
        header[afm_commands[i]['c']] = afm_commands[i]['p']
        i += 1

    # afm comments (if present here):
    afm_comments = []
    while afm_commands[i]['c'] == 'Comment':
        comment_string = ' '.join([afm_commands[i]['c'], afm_commands[i]['p'][0]])
        afm_comments.append(comment_string)
        i += 1
    
    # start char metrics command:
    assert(afm_commands[i]['c'] == 'StartCharMetrics')
    no_of_glyphs = afm_commands[i]['p'][0]
    i += 1

    # metrics data:
    metrix_index_start = i
    metrics = []
    while afm_commands[i]['c'] == 'C':
        # convert a single glyph data:
        # the parameter of C is a sequence of command-parameter pairs
        glyph_metrics = {}
        glyph_ligatures = []
        # ~ log_lib.debug('afm commands', afm_commands[i]['p'])
        for glyph_command in afm_commands[i]['p']:
            # glyph_command is a dictionary, as {'c': commad, 'p': param}
            c = glyph_command['c']
            p = glyph_command['p']
            # add a command c, p to the dictionary of this glyph metrics data:
            if c in ('C', 'WX', 'N'):
                # not a parameter list:
                glyph_metrics[c] = p[0]
            elif c in ('B',):
                # a list of values in case of BB:
                glyph_metrics[c] = p
            else:
                # ~ log_lib.debug('unexpected command %s %s' % (c, p))
                assert(c == 'L')
                glyph_ligatures.append(p)
        if len(glyph_ligatures) == 0:
            glyph_ligatures = None
        glyph_metrics['L'] = glyph_ligatures
            
        metrics.append(glyph_metrics)
        i += 1
    
    if metrix_index_start + no_of_glyphs != i:
        log_lib.critical('wrong number of glyphs metric data [declared]: %d [real]: %d' \
            % (no_of_glyphs, i - metrix_index_start))
        
    # end char metrics command:
    assert(afm_commands[i]['c'] == 'EndCharMetrics')
    i += 1
    # start kern data command:
    assert(afm_commands[i]['c'] == 'StartKernData')
    i += 1
    # start kern pairs command:
    assert(afm_commands[i]['c'] == 'StartKernPairs')
    no_of_kern_pairs = afm_commands[i]['p'][0]
    i += 1
    
    # kern data:
    kerns = []
    kerns_index_start = i
    while afm_commands[i]['c'] == 'KPX':
        kerns.append(afm_commands[i]['p'])
        i += 1
    
    if kerns_index_start + no_of_kern_pairs != i:
        log_lib.critical('wrong number of kern pairs data [declared]: %d [real]: %d' \
            % (no_of_kern_pairs, i - kerns_index_start))

    # end kern pairs command:
    assert(afm_commands[i]['c'] == 'EndKernPairs')
    i += 1
    # end kern data command:
    assert(afm_commands[i]['c'] == 'EndKernData')
    i += 1
    # end font metrics command:
    assert(afm_commands[i]['c'] == 'EndFontMetrics')
    i += 1

    if not (len(afm_commands) == i):
        log_lib.critical('some lines beyond the EndFontMetrics command')
    
    afm = {}
    afm['version'] = version
    afm['initial'] = initial
    afm['header'] = header
    afm['comments'] = afm_comments
    afm['metrics'] = metrics
    afm['kerns'] = kerns
    
    return afm


if __name__ == '__main__':
    import os
    import json
    
    import afm_lib

    command_types = command_syntax_to_command_types(command_syntax)

    for ct in command_types:
        # ~ log_lib.debug(ct, command_types[ct])
        pass

    
    di = 'afm_examples'
    fb = 'afm_in_progress'
    ifn = fb + os.extsep + 'afm'
    ofn = fb + os.extsep + 'json'
    path = os.path.join(di, ifn)

    
    with open(path, 'r') as fh:
        afm_strng = fh.read()

    afm_lines = afm_string_to_line_structures(afm_strng)
    
    for line in afm_lines:
        # ~ log_lib.debug(str(line))
        pass

    afm_commands = line_structures_to_commands(afm_lines)

    sl = []

    for comm in afm_commands:
        # ~ log_lib.debug(str(comm))
        sl.append(str(comm))
        pass
    
    afm_commands_string = '\n'.join(sl)
    
    with open(fb + '.commands.txt', 'w') as fh:
        fh.write(afm_commands_string)

    pass
    
    afm_json = afm_commands_to_afm_structure(afm_commands)
    afm_json_string = json.dumps(afm_json, indent=4, ensure_ascii=False)

    with open(ofn, 'w') as fh:
        fh.write(afm_json_string)


    new_afm_string = afm_lib.afm_json_to_string(afm_json)
    
    with open(fb + '.regenerated.afm', 'w') as fh:
        fh.write(new_afm_string)
    