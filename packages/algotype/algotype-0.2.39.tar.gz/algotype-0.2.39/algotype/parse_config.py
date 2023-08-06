#!/usr/bin/python3
# -*- coding: utf-8 -*-

##!/usr/bin/env python3

# author: Marek Ryćko
__author__ = 'Marek Ryćko <marek@do.com.pl>'

'''
parse a config file
in a simple way:
-- no grammar objects and no parsing according to a grammar,
-- simple lexical grammar,
-- the entire parsing above the lexical level done according
   to a handful of simple functions
and translate it to a json object (dictionary of objects)

05.02.2019 05:11:50
start of the parse_and_test.py

19.04.2019 22:21:43
start from parse_and_test.py
used in color marking of TeX strings

21.04.2019 13:46:21
the parse_config.py practically ready

'''

# standard library
import re
import json

# Algotype:
import algotype.log_lib as log_lib

# ------------------------------------------------------------------------------
# reproducing:
# ------------------------------------------------------------------------------
def wrap(s):
    '''
    represent string like ' abc' as '[ abc]'
    '''
    return '[' + str(s) + ']'

def repr_lines_gen(ll, repr_line):
    '''
    represent a list of lines
    as a string
    where a line is any structure
    for which we have some string representation
    by repr_line
    '''
    if len(ll) == 0:
        return ''
    # decide maximum line number:
    # last line:
    last = ll[-1]
    if isinstance(last, dict) and 'lineno' in last:
        # a line (last line) is a dictionary:
        max_n = last['lineno']
    else:
        max_n = len(ll)
    #
    digits = len(str(max_n))
    # for digits == 5, pattern = '%05d':
    pattern = '%0' + str(digits) + 'd'
    def lineno(ll, i):
        if isinstance(last, dict) and 'lineno' in last:
            r = ll[i]['lineno']
        else:
            r = i + 1
        return r

    r = '\n'.join([(pattern % lineno(ll, i)) + ': ' + repr_line(ll[i]) for i in range(len(ll))])
    return r

def repr_lines(ll):
    '''
    represent a list of lines
    as a string
    '''
    return repr_lines_gen(ll, wrap)

def repr_struct(lt):
    '''
    represent lexical unit list
    and a tail
    as a string
    '''
    lul = lt['lul']
    tail = lt['tail']

    # collecting representation elements as a rl, representation list:
    rl = []
    # lexical unit string:
    lus = ', '.join([repr_lu(lu) for lu in lul])
    # optionally append lus to representation:
    if lus:
        rl.append(lus)
    # optional tail:
    if tail:
        rl.append(wrap(tail))
    r = ' '.join(rl)
    return r

def repr_lu(lu):
    '''
    represent lexical unit
    as a string
    '''
    if 'a' in lu and 'spell' in lu['a'] and not lu['a']['spell']:
        r = "('%s', '%s')" % ('BAD', lu['v'])
    else:
        r = "('%s', '%s')" % (lu['k'], lu['v'])
    
    return r


# ------------------------------------------------------------------------------
# parsing:
# ------------------------------------------------------------------------------
def str_to_lines(s):
    '''
    parse the external structure
    and transform a multiline string s
    to lines
    the result is a list of line strings
    (line numbers are list indexes plus 1)
    
    '''
    r = s.splitlines()
    return r
    
# ~ def head_tail(l, pdl):
def match_one(l, pos, pdl):
    '''
    take a line string l
    read it from the position pos (positions are numbered from 0)
    and split it into head, matching a regular expression from a lexical grammar pdl
    pdl — pattern dictionary list
    return:
        'found' if found
        'head' -- the lexical unit found at the beginning
        'endpos' -- the position within the entire l, after the match
        (maybe not necessary -- tail, not yet processed part of the string)
    '''
    # ~ log_lib.debug('scanning from pos', pos)
    found = False
    for pd in pdl:
        # pd is a pattern dictionary
        # ~ re.match(pattern, string, flags=0)
        # ~ mo = re.match(pd['compiled'], l)
        # ~ mo = re.match(pd['compiled'], l, pos)
        mo = pd['compiled'].match(l, pos)
        if mo:
            found = True
            the_pd = pd
            break
    # found the first possible pattern
    # or not found at all
    if found:
        # prepare the result:
        # the lexical unit:
        f = the_pd['to_value']
        if isinstance(f, int):
            v = mo.group(f)
        else:
            v = f(mo)
        # ~ lu = {'k': the_pd['id'], 'v': mo.group(0)}
        lu = {'k': the_pd['id'], 'v': v}
        tail = l[mo.end(0):]
        r = {'found': True, 'head': lu, 'tail': tail, 'endpos': mo.end(0)}
    else:
        r = {'found': False}
    return r
    
def scan_line(l, i, pdl):
    '''
    scan a line l, of index i, and split it into lexical units
    return a structure (dictionary), containing:
    a list of {'k': k, 'v': v} pairs
    and a tail, where no rule matches
    plus also the original, unstructured line
    its index (counging from 0) and line number (from 1)
    '''
    # lexical unit list:
    lul = []
    # initial tail:
    tail = l
    # initial scanning position within the input string l:
    pos = 0
    while True:
        # stop looping if the tail is empty
        # ~ if len(tail) == 0:
        if pos == len(l):
            break
        # matching result:
        # ~ mr = head_tail(tail, pdl)
        mr = match_one(l, pos, pdl)
        if not mr['found']:
            # match not found
            # stop scanning with the existing tail
            break
        # so a pattern matches:
        lul.append(mr['head'])
        tail = mr['tail']
        pos = mr['endpos']
    # prepare the result:
    r = {'lul': lul, 'tail': tail, 'full': l, 'i': i, 'lineno': i + 1}
    return r

def ll_to_sl(ll, pdl):
    '''
    transform line list
    to a structure list
    where a structure is a list of lexical units and a (hopefully empty) tail
    '''
    sl = []
    for i in range(len(ll)):
        l = ll[i]
        sl.append(scan_line(l, i, pdl))
    return sl
# ------------------------------------------------------------------------------
# lexical grammar functions:
# ------------------------------------------------------------------------------


def pll_to_pdl(pll):
    '''
    translate a pattern list list to a pattern dictionary list
    the pattern dictionary in the resulting list is sth like:
    {'id': 'cs', 'pattern': r'\\(([a-zA-Z]+)|([^a-zA-Z]))',
        'compiled': <compiled pattern>}
        
    each element of the input list, pll, is a 2- or 3-element list:
        [<pattern identifier>, <pattern>]
    or:
        [<pattern identifier>, <pattern>, <how to calculate value>]
        
    the third argument, the “how to calculate value”, if present,
    may be either:
        an integer number >= 0,
        meaning the group number in the matching object
        to be used as the token (lexical unit) value
    or it may be:
        a function (a Python function)
        taking as an argument a matching object
        and returning any value
    Not existing third list element is eqivalent to “0” (integer zero)
    '''
    pdl = []
    for i, pl in enumerate(pll):
        pd = {}
        pd['id'] = pl[0]
        pd['pattern'] = pl[1]
        pd['compiled'] = re.compile(pl[1])
        pd['to_value'] = pl[2] if len(pl) > 2 else 0
        pdl.append(pd)
    return pdl
            
# ------------------------------------------------------------------------------
# parsing:
# ------------------------------------------------------------------------------

def parse_lines(sl):
    '''
    analyse lines represented as structures
    and collect info from significant ones
    in the result structure
    '''
    cl = []
    for l in sl:
        ul = l['lul']
        c = clean_line(ul)
        l['lul'] = c
        # ~ log_lib.debug(str(ul), '-->', c)
        if len(c) > 0:
            cl.append(l)
    # cl is a “clean list”

    # test print:
    for l in cl:
        ul = l['lul']
        # ~ log_lib.debug(l['lineno'], str(ul))
        
    # parse significant lines to [key, value] pairs:
    
    # collect dictionary lines (key-value lines):
    dl = []
    for l in cl:
        kv = parse_line(l['lul'])
        if kv['ok']:
            r = {'lineno': l['lineno'], 'k': kv['k'], 'v': kv['v']}
            dl.append(r)
        else:
            log_lib.error('Error, line ' + str(l['lineno']) + ':', kv['mess'])
            # ~ r = {'lineno': l['lineno'], 'k': kv['k'], 'v': kv['v']}
            # ~ dl.append(r)
    
    for kv in dl:
        # ~ log_lib.debug(kv['lineno'], kv['k'], str(kv['v']))
        pass
        
    # translate the list of kv structures to a single dictionary:
    
    r = {}
    for kv in dl:
        r[kv['k']] = kv['v']
    return r
    

def parse_line(ul):
    '''
    read a lexical unit list
    and return a strucured result
    
    containing the line key (a string at the beginning)
    and the line value — a single object or a list of objects
    '''
    priv = {
        'mess': '',
        'ok': True,
        }
    k = None
    v = None
    
    def err(s):
        priv['ok'] = False
        priv['mess'] = '\n'.join([priv['mess'], s])

    # optional indent to be skipped:
    first = 0
    sk = ul[first]
    if sk['k'] == 'indent':
        log_lib.debug('skipping indent')
        first += 1
        
    # supposed key:
    sk = ul[first]
    if sk['k'] != 'string' and not is_id(sk['v']):
        err("First line element '%s' is not an identifier" % sk['k'])
    else:
        # it is an identifier:
        # the key of a line is a value of the first unit
        k = sk['v']
        first += 1
    
    # ~ log_lib.debug('parsing line with key [%s]' % k)
        
    # skip the optional “is” symbol: equal sign or a colon:
    first = (first + 1) if len(ul) > first and ul[first]['k'] == 'is' else first
       
    # value list; components of the rest of the line (lexical units)
    vl  = ul[first:]
    # now id-s are just strings:
    # ~ nvl = []
    # ~ for v in vl:
        # ~ if v['k'] == 'id':
            # ~ v['k'] = 'string'
    # ~ log_lib.debug('vl', str(vl))
    
    if len(vl) == 0:
        # ~ err('Empty value for the key %s' % str(sk['v']))
        # we may consider treating it as a valid case,
        # with the value of None or of the empty string
        # rather an empty string, that cannot be expressed otherwise
        v = ''
    elif len(vl) == 1 and vl[0]['k'] in ('string', 'boolean', 'number', 'null'):
        # single, final value:
        typ = vl[0]['k']
        val  = vl[0]['v']
        if typ == 'boolean':
            # ~ v = bool(val)
            v = val
        elif typ == 'number':
            # ~ v = int(val)
            v = val
        elif typ == 'null':
            # ~ v = None
            v = val
        else:
            # string
            v  = val
        # ~ v  = r'{' + typ + r'}' + val
    elif len(vl) == 1:
        # just one object, but not the simple one:
        v = repr_unit(vl[0])
    # ~ elif not is_call(vl):
    elif 0:
        # the line does not start from a function call
        # one or more non-final components are treated as to be joined
        # collect the computed values:
        
        x = []
        # ~ v  = str(ul[1:])
        for e in vl:
            #
            # ~ log_lib.debug('e', e)
            x.append(repr_unit(e))
        v = repr_call('j', x)
        
        # ~ log_lib.debug('not call line', str(x))
        # ~ v = el
    # ~ v  = str(ul[1:])
    else:
        r = translate_list(vl)
        # ~ log_lib.debug('call line', str(vl))
        # ~ log_lib.debug(str(r))
        res = r['r']
        if len(res) > 1:
            # ~ err('too many elements in a value')
            # the result will be a list, but it is an error
            # ~ v = res
            v = repr_call('j', res)
            # ~ log_lib.debug(str(res))
        else:
            v = res[0]

    return {'ok': priv['ok'], 'mess': priv['mess'], 'k': k, 'v': v}
    
def translate_list(ul):
    '''
    translate a list of lexiclal units
    up to the closing parenthesis 
    or up to the end of the list
    return the translated result
    and also report the type of end
    and the untranslated tail
    '''
    tail = ul
    # ~ end = ')'
    end = ''
    # result list:
    rl = []
    cont = True
    while len(tail) > 0 and cont:
        # either the first is the closing parenthesis
        # or there is something to do 
        first = tail[0]
        if first['k'] == 'par_end':
            # closing parenthesis
            # rl not changed
            tail = tail[1:]
            end = ')'
            # and we are done
            cont = False
        # ~ elif len(tail) >= 2 and first['k'] == 'string' and is_id(first['v']) \
            # ~ and tail[1]['k'] == 'par_begin':
        elif is_call(tail):
            # we have a situation of a 'function('
            r = translate_list(tail[2:])
            if r['end'] != ')':
                err('no closing parenthesis')
            # anyway: append the result
            f = first['v']
            x = r['r']
            rl.append(repr_call(f, x))
            tail = r['tail']
            cont = True
        else:
            # just a simple translation:
            rl.append(repr_unit(first))
            tail = tail[1:]
            cont = True
    
    return {'r': rl, 'end': end, 'tail': tail}

def repr_unit(u):
    '''
    represent unit u
    as a json config input language component
    '''
    # ~ log_lib.debug('representing unit', str(u))
    k = u['k']
    v = u['v']
    if k == 'use':
        # v is something like $abc, return ['u', 'abc']
        # ~ r = ['u', v[1:]]
        # ~ log_lib.debug(v)
        r = repr_call('u', [v[1:]])
        # ~ log_lib.debug('1 represent [%s, %s] as %s' % (k, v, str(r)))
    elif k == 'call':
        # v is something like @abc, return ['abc']
        # ~ r = [v[1:]]
        r = repr_call(v[1:], [])
    elif k == 'string':
        r = v
    else:
        r = str(v)
    # ~ if k == 'use':
        # ~ log_lib.debug('represent [%s, %s] as %s' % (k, v, str(r)))
    return r
    
def repr_call(f, x):
    '''
    represent in the result a function call,
    where f is the function name (id) and x is the function parameter
    usually x is a list of objects
    '''
    r = [f]
    r.extend(x)
    
    # ~ r = {'f': f, 'x': x}
    return r
    
    
def clean_line(ul):
    '''
    remove all the skippable elements of the line
    '''
    return [u for u in ul if not skippable(u)]
    
def skippable(u):
    '''
    return true if the lexical unit u is skippable
    '''
    k = u['k']
    return k in ('space', 'comment')
    
def is_id(s):
    '''
    check if a string is an id (identifier)
    '''
    pat = r'([a-zA-Z\_][a-zA-Z0-9\_]*)'
    com = re.compile(pat)
    mo = re.match(com, s)
    r = True if mo else False
    return r
    
def is_call(tail):
    '''
    check if a lexical unit list tail starts from a function call,
    i.e. from two units: 'some_id', '('
    '''
    if len(tail) < 2:
        res = False
    else:
        first = tail[0]
        res = first['k'] == 'string' and is_id(first['v']) \
            and tail[1]['k'] == 'par_begin'
    return res

# ------------------------------------------------------------------------------
# filtering:
# ------------------------------------------------------------------------------
def filter_lines(sl, fi):
    '''
    select only lines (structures)
    satisfying condition fi(s)
    '''
    r = [s for s in sl if fi(s)]
    return r

def nonempty_tail(s):
    '''
    True if tail in struct is nonempty
    '''
    return len(s['tail']) > 0


# ------------------------------------------------------------------------------
# initializations and config:
# ------------------------------------------------------------------------------


def mo_to_boolean(mo):
    '''
    in this lexical analyser it is sufficient to test one way:
    '''
    return mo.group(0).lower() == 'true'
    
def mo_to_str(mo):
    # ~ log_lib.debug(wrap(mo.group(1)))
    # ~ log_lib.debug(wrap(mo.group(2)))
    s = mo.group(1) if mo.group(2) is None else mo.group(2)
    return s

# lexical grammar; pattern list list:

pll = [
    ['comment', r'(\%|\#).*$'],
    ['boolean', r'((T|t)rue|(F|f)alse)', mo_to_boolean],
    ['null', r'((N|n)one|(N|n)ull)', lambda x: None],


    ['string', r'([a-zA-Z\_\-\\\/\:\.\,0-9]+)|\'([a-zA-Z\_\-\\\/\:\.\,0-9\s]+)\'', mo_to_str],
    ['use', r'\$([a-zA-Z\_][a-zA-Z0-9\_]*)'],
    # ~ ['call', r'\@([a-zA-Z\_][a-zA-Z0-9\_]*)'],

    # in order not to split 01abc into 01 and abc:
    ['number', r'([0-9]+)', lambda mo: int(mo.group(0))],

    # ~ ['is', r'(\=|\:)'],
    ['is', r'\='],

    ['par_begin', r'[\(]'],
    ['par_end', r'[\)]'],
    ['indent', r'^\s+'],
    ['space', r'\s+'],
]



# ------------------------------------------------------------------------------
# main parsing/translation:
# ------------------------------------------------------------------------------

def parse(s):
    '''
    parse a string s
    and return a json structure
    '''
    ll = str_to_lines(s)
    # ~ log_lib.debug(repr_lines(ll))

    pdl = pll_to_pdl(pll)

    # parse to a structure list:
    sl = ll_to_sl(ll, pdl)
    # ~ for l in sl:
        # ~ log_lib.debug(str(l))
    # ~ log_lib.debug(repr_lines_gen(sl, repr_struct))

    nt = filter_lines(sl, nonempty_tail)
    # ~ log_lib.debug('filtered lines:', repr_lines_gen(nt, repr_struct))

    j = parse_lines(sl)

    return j
    
