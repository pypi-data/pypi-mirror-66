#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
afm_lib.py
a library of service functions
for transforming metric font data taken from json_font
creating a json representation of metric data
and serializing them as AFM files (Adobe Font Metric)

Marek Ryćko

start as a copy of parse_eps
03.01.2020 14:33:58
'''

# standard library:
import operator
# for afm generation timestamp:
from datetime import datetime

# Algotype:
from algotype.goadb_lib import glyph_name_to_type_one
# prints converted to log_lib function calls:
import algotype.log_lib as log_lib

# ------------------------------------------------------------------------------
# general utilities:
# ------------------------------------------------------------------------------
def number_to_string(n):
    '''
    Represent and integer or floating point number according to configuration.
    
    If current config forces integer values the floats are rounded to integers.
    Integers are represented with minimal number of digits.
    Floats are represented with minimum trailing zeros.
    '''
    # this config can be changed or set somewhere else:
    rounding = False
    if rounding:
        n = round(n)
    if isinstance(n, int) or float(round(n)) == n:
        # n is integer or is a float equal to integer
        s = '%d' % n
    else:
        # n is a non-integer float
        s = ('%f' % n).rstrip('0').rstrip('.')
    return s

def bounding_box_to_string(bb):
    bs = ' '.join([number_to_string(bb[i]) for i in range(4)])
    return bs
    
def value_to_string(v):
    '''
    convert a value to a string
    '''
    if isinstance(v, (int, float)):
        s = number_to_string(v)
    elif isinstance(v, bool):
        s = str(v).lower()
    elif isinstance(v, str):
        s = v
    return s
    
def parameters_to_string(vl):
    '''
    Convert a list vl of values to a string.
    
    in the resulting string the string representation of values
    are joined/separated with spaces
    '''
    
    s = ' '.join([value_to_string(v) for v in vl])
    return s
    
def target_glyph_name(goadb, glyph_name):
    '''
    translate glyph name in a proper way
    from metapost/eps glyph names
    to the target (PFB/Type1) glyph names
    
    In GOADB file for the Type1 (PFB, AFM) purpose
    there is to be the translation:
        -- if in column of index -1 (the last) is PFBNAME:
            -- use column of index 1 (the second)
        -- else:
            -- translate from column of index 1 to column of index 0
            
    no, no, no.
    
    the conversion here, for LM fonts, should be transparent
    
    '''
    target = glyph_name

    if 0:
        target = glyph_name_to_type_one(goadb, glyph_name)
        if target != glyph_name:
            # ~ log_lib.debug('translated glyph mpost to Type1: %s --> %s' % \
                # ~ (glyph_name, target))
            pass
        
        target = '<%s>' % target
        # ~ target = '[%s]' % glyph_name
    return target

# ------------------------------------------------------------------------------
# collecting AFM data from a json font:
# ------------------------------------------------------------------------------

def json_font_to_json_afm(jf):
    '''
    Translate a font, as a json structure, to AFM represented as a json structure.
    '''
    # afm structure (to be further serialized to AFM string and written as a file)
    # will be represented as a dictionary of several groups of data
    
    # the afm data structure will contain:
    # 1. header data
    # 2. font specific (TeX oriented) comments
    # 3. character metric data
    # 4. kern pairs
    
    # 0.
    initial = json_font_to_initial_comments(jf)
    
    # 1.
    # collecting the header data
    header = json_font_to_json_afm_header(jf)
    
    # 2.
    # collecting font specific comments:
    afm_comments = json_font_to_afm_tfm_comments(jf)
    
    #3.
    # collecting character metric data:
    metrics = json_font_to_json_char_metrics(jf)
    
    # 4.
    # collecting kern pairs:
    kerns = json_font_to_kern_list(jf)
    
    # putting the data all together in a resulting dictionary:

    afm = {}
    afm['initial'] = initial
    afm['header'] = header
    afm['comments'] = afm_comments
    afm['metrics'] = metrics
    afm['kerns'] = kerns

    return afm
    
def json_font_to_json_afm_header(jf):
    '''
    Translate a font, as a json structure, to a header AFM data.
    '''
    # afm structure (to be further serialized to AFM string and written as a file)
    # will be represented as a dictionary of several groups of data
    
    # the afm data structure will contain:
    # 1. header data
    # 2. font specific (TeX oriented) comments
    # 3. character metric data
    # 4. kern pairs
    
    # collect header data
    header = {}
    
    # take values from transformed OTI attributes,
    # rather than close to OTI syntax:
    header['FontName'] = jf['par']['attr']['fontname']
    header['FullName'] = jf['par']['attr']['fullname']
    header['FamilyName'] = jf['par']['attr']['familyname']
    header['Weight'] = jf['par']['attr']['weight']
    header['Notice'] = jf['par']['attr']['copyright']
    # in OTI and json_font italicangle is real (float)
    header['ItalicAngle'] = jf['par']['attr']['italicangle']
    if 'fixedpitch' in jf['par']['attr']:
        # no more in the 'attr' item of parsed attributes
        ItalicAngle_string = jf['par']['attr']['fixedpitch']
    else:
        ItalicAngle_string = jf['oti_par']['FIXED_PITCH']
    header['IsFixedPitch'] = True if ItalicAngle_string == 'true' else False
    if 'upos' in jf['par']['attr']:
        # should be within the results of parsing OTI to json_font:
        underline_position_string = jf['par']['attr']['upos']
    else:
        underline_position_string = jf['oti_par']['UNDERLINE_POSITION']
    header['UnderlinePosition'] = float(underline_position_string)
    header['UnderlineThickness'] = jf['par']['attr']['uwidth']
    header['Version'] = jf['par']['attr']['version']
    if 'encoding_scheme' in jf['par']['attr']:
        # no more in the 'attr' item of parsed attributes
        encoding_scheme_string = jf['par']['attr']['encoding_scheme']
    else:
        encoding_scheme_string = jf['oti_par']['ENCODING_SCHEME']
    header['EncodingScheme'] = encoding_scheme_string
    
    # FontBBox:
    bbox = json_font_to_font_bbox(jf)
    header['FontBBox'] = bbox
    
    if 'cap_height' in jf['par']['attr']:
        # no more in the 'attr' item of parsed attributes
        cap_height_float = jf['par']['attr']['cap_height']
    else:
        cap_height_float = float(jf['oti_par']['CAPHEIGHT'])
    header['CapHeight'] = cap_height_float

    if 'x_height' in jf['par']['attr']:
        # no more in the 'attr' item of parsed attributes
        x_height_float = jf['par']['attr']['x_height']
    else:
        x_height_float = float(jf['oti_par']['XHEIGHT'])
    header['XHeight'] = x_height_float

    if 'ascender' in jf['par']['attr']:
        # no more in the 'attr' item of parsed attributes
        ascender_float = jf['par']['attr']['ascender']
    else:
        ascender_float = float(jf['oti_par']['ASCENDER'])
    header['Ascender'] = ascender_float

    if 'descender' in jf['par']['attr']:
        # no more in the 'attr' item of parsed attributes
        descender_float = jf['par']['attr']['descender']
    else:
        descender_float = float(jf['oti_par']['DESCENDER'])
    header['Descender'] = descender_float
    
    # compare some of the calculated values
    # to those following the AFM specification
    # https://www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5004.AFM_Spec.pdf
    
    # CapHeight:
    # (Optional.) Usually the y-value of the top of the capital H.
    # If this font program contains no capital H,
    # this keyword might be missing or numbermight be 0.
    
    # XHeight:
    # (Optional.) Typically the y-value of the top of the lowercase x.
    # If this font program contains no lowercase x,
    # this keyword might be missing or numbermight be 0.
    
    # Ascender:
    # (Optional.) For roman font programs: usually the y-value of
    # the top of the lowercase d. If this font program contains no lowercase d,
    # this keyword might be missing or number might be 0
    
    # Descender:
    # (Optional.) For roman font programs: typically the y-value of
    # the bottom of the lowercase p. If this font program contains no
    # lowercase p, this keyword might be missing or number might be 0.
    
    
    
    # the Y char measurments within the oti_gly parameter of json font:
    
    '''
    "oti_glyphs": {
        "A": {
            "CODE": "65",
            "EPS": "165",
            "WD": "755.55556 HT 686.11111 DP 0 IC 0",
            "HSBW": "755.55556",
            "BBX": "35 0 720 698",
            "KPX": [
                [
                    "C",
                    "-27.778"
                ],
    '''
    
    # the Y char measurments within the glyphs parameter of json font:
    '''
    "glyphs": {
        "A": {
            "codepoint": null,
            "code": "65",
            "glyph_name": "A",
            "metrics": {
                "width": 755.55556,
                "textheight": 686.11111,
                "textdepth": 0
            },

    '''

    # so the cap height following the specification is:
    cap_height_spec = float(jf['glyphs']['H']['metrics']['textheight'])
    cap_height_info = 'CapHeight [spec value]: %s [oti value]: %s' % \
        (number_to_string(cap_height_spec), number_to_string(cap_height_float))
    log_lib.debug(cap_height_info)
    
    # so the x height following the specification is:
    x_height_spec = float(jf['glyphs']['x']['metrics']['textheight'])
    x_height_info = 'XHeight [spec value]: %s [oti value]: %s' % \
        (number_to_string(x_height_spec), number_to_string(x_height_float))
    log_lib.debug(x_height_info)
    
    # so the ascender following the specification is:
    ascender_spec = float(jf['glyphs']['d']['metrics']['textheight'])
    ascender_info = 'Ascender [spec value]: %s [oti value]: %s' % \
        (number_to_string(ascender_spec), number_to_string(ascender_float))
    log_lib.debug(ascender_info)
    
    # so the descender following the specification is:
    descender_spec = float(jf['glyphs']['p']['metrics']['textdepth'])
    descender_info = 'Descender [spec value]: %s [oti value]: %s' % \
        (number_to_string(descender_spec), number_to_string(descender_float))
    log_lib.debug(descender_info)
    

    '''
    example header data:

    Comment Generated by FontForge 20170924
    Comment Creation Date: Mon Dec 30 18:10:35 2019
    FontName LMRomanDemi10-Regular
    FullName LMRomanDemi10-Regular
    FamilyName LMRomanDemi10
    Weight Demi
    Notice (Copyright 2003--2009 by B. Jackowski and J.M. Nowacki (on behalf of TeX USERS GROUPS).)
    ItalicAngle 0
    IsFixedPitch false
    UnderlinePosition -100
    UnderlineThickness 60
    Version 2.004
    EncodingScheme FontSpecific
    FontBBox -442 -295 1406 1136
    CapHeight 686
    XHeight 444
    Ascender 697
    Descender -200
    '''
    
    # new style structure: putting all the header parameters
    # to a list
    # (FontBBox is already a list of values)
    
    new_header = {}
    for k, v in header.items():
        if k == 'FontBBox':
            new_v = v
        else:
            new_v = [v]
        new_header[k] = new_v
        
    return new_header
    
    
def json_font_to_initial_comments(jf):
    '''
    Possibly making use of the json font -- generate initial comments.
    
    In afm files generated by Fontforge the comments looked like this:
    Comment Generated by FontForge 20170924
    Comment Creation Date: Mon Dec 30 18:10:35 2019
    
    '''
    sl = []
    sl.append('Comment Generated by Algotype')
    
    now = datetime.now()
    now_string = now.strftime('%B %d, %Y, %H:%M:%S')
    
    sl.append(f'Comment Creation Date: {now_string}')
    
    return sl
    

def json_font_to_font_bbox(jf):
    '''
    From the font (json) data calculate the font bounding box.
    '''

    def move_if_font_rel_glyph(rel, i):
        if font_bounding_box[i] is None or \
                rel(font_bounding_box[i], bounding_box[i]):
            font_bounding_box[i] = bounding_box[i]

    # the extremum values are yet unknown
    font_bounding_box = [None, None, None, None]
    for glyph in jf['glyphs'].values():
        # making shallow copy:
        old_font_bounding_box = list(font_bounding_box)
        # from the glyph info read the bounding box:

        # at least one glyph bounding box is required
        if 'HiResBoundingBox' in glyph['meta']:
            bounding_box = glyph['meta']['HiResBoundingBox']
        else:
            bounding_box = glyph['meta']['BoundingBox']

        # change the extremum values within the font bounding box:
    
        move_if_font_rel_glyph(operator.gt, 0)
        move_if_font_rel_glyph(operator.gt, 1)
        move_if_font_rel_glyph(operator.le, 2)
        move_if_font_rel_glyph(operator.le, 3)
        
        if 0:
            if tuple(old_font_bounding_box) != tuple(font_bounding_box):
                # we have a new bounding box
                log_lib.debug('%s: %s --> %s' % (bounding_box, old_font_bounding_box,
                    font_bounding_box))

    return font_bounding_box
    

def json_font_to_kern_list(jf):
    '''
    From the font (json) data
    calculate the kern pairs
    labelled using the mpost/eps names
    '''
    json_font_kerns = jf['kerns']
    # json_font_kerns is a dict of dicts
    
    kern_list = []
    for left_glyph_name, kern_dict in json_font_kerns.items():
        for right_glyph_name, kern_value in kern_dict.items():
            # prepare and append to the list
            # the logical information about the pair of glyph names
            # and the kern value
            left_glyph_name_translated = target_glyph_name(jf['goadb'], \
                left_glyph_name)
            right_glyph_name_translated = target_glyph_name(jf['goadb'], \
                right_glyph_name)
            kern_triple = [left_glyph_name_translated, \
                right_glyph_name_translated, kern_value]
            kern_list.append(kern_triple)
            
    # the kern list is collected
    # we will sort it in a neat way
    
    def key(kp):
        '''
        what is the sorting key of a single kern pair, kp
        
        kern pair info, kp, is in fact a triple:
            [left_name, right_name, kern_value]
        '''
        return tuple(kp)
        
    res = sorted(kern_list, key=key)


    return res
    
def json_font_to_afm_tfm_comments(jf):
    '''
    a maintained copy of this function used to be in ffdkm,
    but we tend to make the one in afm_lib — the only valid and maintained
    
    jf, the json font, contains a parsed oti structure and oti is used here
    (oti is one of the results of metaposting)
    
    '''
    oti = jf['oti_par']
    res = []
    if 'PFM_NAME' in oti:
        res.append('Comment PFM parameters: %s %s %s %s' % (oti['PFM_NAME'], 
            oti['PFM_BOLD'], oti['PFM_ITALIC'], oti['PFM_CHARSET']))
    if 'DESIGN_SIZE' in oti:
        res.append('Comment TFM designsize: %s (in points)' % (oti['DESIGN_SIZE']))
    if 'FONT_DIMEN' in oti:
        fd = oti['FONT_DIMEN']
        fn = oti['DIMEN_NAME']
        for i in range(256):
            s = str(i)
            if s in fd:
                res.append('Comment TFM fontdimen %2s: %-10s %s' % (s, fd[s], fn[s]))
    if 'HEADER_BYTE' in oti:
        hb = oti['HEADER_BYTE']
        for i in ('9', '49', '72'):
            if i in hb:
                res.append('Comment TFM headerbyte %2s: %s' % (i, hb[i]))
    return res
    
def json_font_to_ligatures(jf):
    '''
    from the json font collect information about ligatures
    to be further used in preparing char metrics data
    '''
    ligatures = {}
    
    # so far the ligature data is stored in partially parsed oti structure
    oti_glyphs = jf['oti_glyphs']
    
    for name in oti_glyphs:
        # possibly collect ligature data also:
        # the ligature data for the glyph of an mpost/eps name
        # may or may not exist
        
        try:
            raw_lig_data = oti_glyphs[name]['LIG']
        except:
            raw_lig_data = None
            
        if raw_lig_data is not None:
            # the raw_lig_data for the name 'f_k' is 'f k'
            lig_names = raw_lig_data.split()
            # ~ log_lib.debug('Raw ligature for %s: %s' % (name, str(lig_names)))
        else:
            pass
            lig_names = None
    
        if lig_names is not None:
            # lig_names should be a list of two elements
            if not (len(lig_names) == 2):
                log_lib.warning('wrong number of ligature components in OTI: %s' % \
                    str(lig_names))
            # lig names is a list of two elements:
            if lig_names[0] not in ligatures:
                ligatures[lig_names[0]] = []
            # append ligature info:
            ligatures[lig_names[0]].append([lig_names[1], name])
            # ~ log_lib.debug('preparing ligature info: %s: %s' % \
                # ~ (lig_names[0], str(ligatures[lig_names[0]])))
                
    # sort the value of each ligature entry
    # the value is a list of name pair
    
    # the kern list is collected
    # we will sort it in a neat way
    
    def key(li):
        '''
        what is the sorting key of a single ligature info
        
        ligature info, li, is a pair of glyph name:
            [right_name, result_name]
        '''
        return tuple(li)
        # ~ return tuple(li)
        
    res = {}
    for k, v in ligatures.items():
        new_v = sorted(v, key=key)
        # just for test:
        # ~ new_v = sorted(v, key=key, reverse=True)
        res[k] = new_v
    
    return res
    
def json_font_to_json_char_metrics(jf):
    '''
    Translate a font, as a json structure, to a list of character metrical info.
    
    The returned list is sorted in some fixed, neat way.
    '''

    ligatures = json_font_to_ligatures(jf)

    metrics = []
    for glyph in jf['glyphs'].values():
        # collect the metrics info for the glyph glyph:

        name = glyph['glyph_name']
        
        # reading codepoint is pointless; so far it is always -1
        # as of 05.01.2020 20:48:46:
        codepoint  = glyph['codepoint']
        codepoint  = glyph['codepoint']
        # we have None/null in json, denoted as -1 in afm:
        codepoint = -1 if codepoint is None else codepoint
        
        # code taken from oti:
        if 'code' in glyph:
            code = glyph['code']
        else:
            log_lib.debug(name, jf['glyphs'][name])
            log_lib.debug(jf['oti_par']['glyphs'][name])
            # ~ code = jf['glyphs'][name]['CODE']

        wx = glyph['metrics']['width']
        if 'HiResBoundingBox' in glyph['meta']:
            bounding_box = glyph['meta']['HiResBoundingBox']
        else:
            bounding_box = glyph['meta']['BoundingBox']
            
        if name in ligatures:
            # ~ ligature_data = ligatures[name]
            ligature_data = []
            for el in ligatures[name]:
                el_data = [target_glyph_name(jf['goadb'], el[0]), \
                    target_glyph_name(jf['goadb'], el[1])]
                ligature_data.append(el_data)

            # ~ log_lib.debug('adding ligature info for %s: %s' % \
                # ~ (name, str(ligature_data)))
        else:
            ligature_data = None
            
        glyph_metrics = {
            # ~ 'C': codepoint,
            # 05.01.2020 21:30:27:
            'C': int(code),
            'WX': wx,
            'N': target_glyph_name(jf['goadb'], name),
            'B': bounding_box,
            'L': ligature_data,
        }
        metrics.append(glyph_metrics)
        
    # the metrics list is collected
    # we will sort it in a neat way
    
    def key(gm):
        '''
        what is the sorting key of a single glyph metrics, gm
        '''
        # first the group of glyphs possesing the code, then the rest:
        group = 0 if gm['C'] >= 0 else 1
        # then the code within the first group
        # (it will be always -1 within the second)
        code = gm['C']
        # for no-code glyphs the name counts:
        name = gm['N']
        
        return (group, code, name)
        
    res = sorted(metrics, key=key)
    
    return res
    
# ------------------------------------------------------------------------------
# serializations of logical afm data as sequences of lines (strings):
# ------------------------------------------------------------------------------

def header_to_lines(header):
    '''
    Represent the afm header structure as a series of lines-strings.
    
    Represent the afm header structure,
    as calculated by json_font_to_json_afm_header(jf)
    as a series of lines-strings.
    '''
    sl = []
    for k, vl in header.items():
        s = parameters_to_string(vl)
        sl.append('%s %s' % (k, str(s)))

    return sl

def glyph_metrics_to_lines(metrics):
    '''
    Represent the glyph metrics structure as a series of lines-strings.
    
    Represent the glyph metrics,
    as calculated by json_font_to_json_char_metrics(jf)
    as a series of lines-strings.
    '''
    sl = []
    for d in metrics:
        c = 'C %d' % d['C']
        w = 'WX ' + number_to_string(d['WX'])
        n = 'N %s' % d['N']
        b = 'B ' + bounding_box_to_string(d['B'])
        elements = [c, w, n, b]
        # add the optional ligature info:
        lig = d['L']
        if lig is not None:
            lig_string = ' ; '.join(['L %s %s' % (el[0], el[1]) \
                for el in lig])
            elements.append(lig_string)

        s = ' ; '.join(elements)

        # complete the string by adding ' ;' at the end:
        s += ' ;'
            
        sl.append(s)
    return sl

def kern_list_to_lines(kern_info):
    '''
    Represent the logical info in a kern_list structure to a series of lines.
    '''
    sl = []
    for l in kern_info:
        kern_value = number_to_string(l[2])
        names = 'KPX %s %s' % (l[0], l[1])
        kern_line = ' '.join([names, kern_value])
        sl.append(kern_line)
    return sl

# ------------------------------------------------------------------------------
# collecting the serializations of areas of afm data
# and serializing all of them as a single sequence of lines (strings):
# ------------------------------------------------------------------------------

def afm_json_to_lines(afm_json):
    '''
    Represent the afm json structure as a series of lines-strings.
    
    Represent the afm header structure,
    as calculated by json_font_to_json_afm_header(jf)
    as a series of lines-strings.
    '''
    # string list:
    sl = []
    sl.append('StartFontMetrics 4.1')
    
    # initial comments:
    sl.extend(afm_json['initial'])
    
    sl.extend(header_to_lines(afm_json['header']))
    sl.extend(afm_json['comments'])
    # 
    glyph_metrics_list = afm_json['metrics']
    sl.append('StartCharMetrics %d' % len(glyph_metrics_list))
    sl.extend(glyph_metrics_to_lines(glyph_metrics_list))
    sl.append('EndCharMetrics')
    
    kern_pairs_list = afm_json['kerns']
    sl.append('StartKernData')
    sl.append('StartKernPairs %d' % len(kern_pairs_list))
    sl.extend(kern_list_to_lines(kern_pairs_list))
    sl.append('EndKernPairs')
    sl.append('EndKernData')
    
    sl.append('EndFontMetrics')
    
    return sl
    

# ------------------------------------------------------------------------------
# final transformation of a series of lines
# to a single (multiline) string representing the AFM data
# ------------------------------------------------------------------------------

def afm_json_to_string(afm_json, rounding=False):
    '''
    Represent the afm_json structure as a multiline string.
    
    If rounding is True, the float numbers are rounded in serialization
    to the nearest integer value.
    '''
    # set a global afm serialization config:
    afm_config['rounding'] = rounding
    
    sl = afm_json_to_lines(afm_json)
    res = '\n'.join(sl)
    return res
    
afm_config = {
    'rounding': False,
}

if __name__ == '__main__':

    afm_json = json_font_to_json_afm(jf)
    s = afm_json_to_string(afm_json)
    pass
