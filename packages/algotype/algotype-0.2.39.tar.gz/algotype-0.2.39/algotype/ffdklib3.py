#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
python3 library of oti services
(consider renaming it to oti_lib)
mainly the oti file parser
'''



import re

# Algotype:
import algotype.log_lib as log_lib

FFattrConst = {
  'hhea_ascent_add': 0,
  'hhea_descent_add': 0,
  'os2_winascent_add': 1,
  'os2_windescent_add': 1,
  'os2_typoascent_add': 0,
  'os2_typodescent_add': 0,
  'os2_winascent': 0,
  'os2_windescent': 0,
}

OTItoFFattrI = {
'ADL_ASCENDER' : 'ascent',
'ADL_DESCENDER': 'descent',
'ADL_LINESKIP':('os2_typolinegap', 'hhea_linegap'),
# 'ascender' and 'descender' added around 04.01.2020:
#'ASCENDER'  :  ('os2_typoascent', 'hhea_ascent', 'ascender'),
#'DESCENDER' :  ('os2_typodescent', 'hhea_descent', 'descender'),
# 'ascender' and 'descender' removed 25.03.2020 12:57:50:
'ASCENDER'  :  ('os2_typoascent', 'hhea_ascent'),
'DESCENDER' :  ('os2_typodescent', 'hhea_descent'),
# 'CAPHEIGHT': 'capHeight',
# MR, turned on 04.01.2020 00:13:25:
# MR, turned off 25.03.2020 12:44:49:
#'CAPHEIGHT': 'cap_height',
# 'XHEIGHT': 'xHeight',
# MR, turned on 04.01.2020 00:18:07:
# MR, turned of 25.03.2020 12:45:13:
# 'XHEIGHT': 'x_height',
# 'BLUE_FUZZ': '',
# 'BLUE_SCALE': '',
# 'BLUE_SHIFT': '',
# 'BLUE_VALUES ': '',
# 'FONT_DIMEN'
'DESIGN_SIZE': 'design_size',
'ITALIC_ANGLE': 'italicangle',
# there was an error: extra space within the string:
# 'UNDERLINE_POSITION ': 'upos',
# corrected by mr, 03.01.2020 23:48:10:
'UNDERLINE_POSITION': 'upos',
'UNDERLINE_THICKNESS': 'uwidth',
}

OTItoFFattrS = {
'AUTHOR': 'copyright',
'FONT_NAME': 'fontname',
'FULL_NAME': 'fullname',
'FAMILY_NAME': 'familyname',
# 'STYLE_NAME': '',
# 'SIZE_NAME': '',
#! 'CREATION_DATE': '',
# 'DIMEN_NAME'
# restored by mr, 03.01.2020 23:55:59:
# turned off again by mr, 25.03.2020 12:47:11:
# 'ENCODING_SCHEME': 'encoding_scheme', 
# restored by mr, 03.01.2020 23:32:39:
# turned off again by mr, 25.03.2020 12:47:11:
# 'FIXED_PITCH': 'fixedpitch',
# 'FORCE_BOLD': '',
# 'HEADER_BYTE'
# 'PFM_BOLD': '',
#! 'PFM_CHARSET': '',
# 'PFM_ITALIC': '',
# 'PFM_NAME': '',
'VERSION': 'version',
'WEIGHT': 'weight',
}

OTItoSFNT = {
'AUTHOR': 'Copyright',
'FAMILY_NAME': 'Family',
'STYLE_NAME': 'SubFamily',
'FULL_NAME': 'Fullname',
# 'UniqueID',
# 'Version',
'FONT_NAME': 'PostScriptName',
# 'Trademark',
# 'Manufacturer',
# 'Designer',
# 'Descriptor', 
# 'Vendor URL', 
# 'Designer URL', 
# 'License', 
# 'License URL', 
# 'Preferred Family', 
# 'Preferred Styles', 
# 'Compatible Full', 
# 'Sample Text', 
# 'CID findfont Name', 
# 'WWS Family', 
# 'WWS Subfamily', 
} 

MATH_Const = [
'AxisHeight',
'MathLeading',
#
'ScriptPercentScaleDown',
'ScriptScriptPercentScaleDown',
'SubscriptShiftDown',
'SubscriptBaselineDropMin',
'SubscriptTopMax',
'SubSuperscriptGapMin',
'SuperscriptShiftUp',
'SuperscriptShiftUpCramped',
'SuperscriptBaselineDropMax',
'SuperscriptBottomMin',
'SuperscriptBottomMaxWithSubscript',
'SpaceAfterScript',
#
'FractionRuleThickness',
'FractionNumeratorShiftUp',
'FractionNumeratorDisplayStyleShiftUp',
'FractionNumeratorGapMin',
'FractionNumeratorDisplayStyleGapMin',
'FractionDenominatorShiftDown',
'FractionDenominatorDisplayStyleShiftDown',
'FractionDenominatorGapMin',
'FractionDenominatorDisplayStyleGapMin',
'SkewedFractionHorizontalGap',
'SkewedFractionVerticalGap',
#
'StackBottomShiftDown',
'StackBottomDisplayStyleShiftDown',
'StackTopShiftUp',
'StackTopDisplayStyleShiftUp',
'StackGapMin',
'StackDisplayStyleGapMin',
'StretchStackBottomShiftDown',
'StretchStackTopShiftUp',
'StretchStackGapAboveMin',
'StretchStackGapBelowMin',
#
'RadicalRuleThickness',
'RadicalVerticalGap',
'RadicalDisplayStyleVerticalGap',
'RadicalExtraAscender',
'RadicalDegreeBottomRaisePercent',
'RadicalKernBeforeDegree',
'RadicalKernAfterDegree',
#
'AccentBaseHeight',
'FlattenedAccentBaseHeight',
#
'OverbarRuleThickness',
'OverbarVerticalGap',
'OverbarExtraAscender',
'UnderbarRuleThickness',
'UnderbarVerticalGap',
'UnderbarExtraDescender',
#
'DisplayOperatorMinHeight',
'DelimitedSubFormulaMinHeight',
'LowerLimitGapMin',
'LowerLimitBaselineDropMin',
'UpperLimitGapMin',
'UpperLimitBaselineRiseMin',
'MinConnectorOverlap',
]


def read_oti(otiname): 
    try:
        # open function, not “file”, 21.02.2019 03:28:56:
        foti = open(otiname, 'r')
    except IOError:
        log_lib.critical("Couldn't find OTI file: %s" % otiname)
        return {'font': {}, 'glyphs': {}, 'list': []}
    oti_fnt = {} 
    oti_gly = {} 
    gly_lst = []
    for line in foti.readlines():
        # remove DOS/UNIX EOLs:
        line = line.rstrip()
        # line = re.sub(' *#.*$', '', line)
        # MR, 21.04.2020 22:54:27:
        line = re.sub(r'\s*(\#|\%).*$', '', line)
        if line == '':
            continue
        if (line.find('FNT ') == 0):
            linem = re.match(r'^FNT[ \t]+([A-Z_]+)([0-9]*)[ \t]+(.+)$', line)
            if linem:
                if linem.group(2):
                    # if that attribute is not yet in the oti font,
                    # insert the empty dict:
                    if  linem.group(1) not in oti_fnt:
                        oti_fnt[linem.group(1)] = {}
                        
                    # put the attribute to the dict:
                    if linem.group(2) not in oti_fnt[linem.group(1)]:
                        oti_fnt[linem.group(1)][linem.group(2)] = linem.group(3)
                    else:
                        # ~ log_lib.warning("Duplicated atribute [1st case] in OTI:\n  %s" % line)
                        # overwrite the previous value:
                        # (to adjust to the situation found in OTI files
                        # in LM fonts)
                        # 12.10.2019 20:45:43:
                        oti_fnt[linem.group(1)][linem.group(2)] = linem.group(3)
                else:
                    if linem.group(1) not in oti_fnt:
                        oti_fnt[linem.group(1)] = linem.group(3)
                    else:
                        # ~ log_lib.warning("Duplicated atribute [2nd case] in OTI:\n  %s" % line)
                        # overwrite the previous value:
                        # (to adjust to the situation found in OTI files
                        # in LM fonts)
                        # 12.10.2019 20:45:43:
                        oti_fnt[linem.group(1)] = linem.group(3)
            else:
                log_lib.warning("Unrecognized line in OTI:\n  %s" % line)
        elif (line.find('GLY ')==0):
            linem = re.match(r'^GLY[ \t]+([A-Za-z0-9\._]+)[ \t]+([A-Z_\-]+)[ \t]+(.+)$', line)
            if linem:
                gly=linem.group(1)
                if gly not in oti_gly:
                    oti_gly[gly]={}
                    gly_lst.append(gly)
                if linem.group(2)=='KPX':
                    if 'KPX' not in oti_gly[gly]:
                        oti_gly[gly]['KPX']=[]
                    oti_gly[gly]['KPX'].append(linem.group(3).split())
                elif linem.group(2)=='ANCHOR':
                    if 'ANCHOR' not in oti_gly[gly]:
                        oti_gly[gly]['ANCHOR']={}
                    anch=linem.group(3).split()    
                    if anch[0] not in oti_gly[gly]['ANCHOR']:
                        oti_gly[gly]['ANCHOR'][anch[0]]={}
                    oti_gly[gly]['ANCHOR'][anch[0]][anch[1]]=(anch[2],anch[3])
                elif linem.group(2).find('HINT')>-1:
                    pass
                else:
                    if linem.group(2) not in oti_gly[gly]:
                        pass
                    else:
                        # ~ log_lib.warning("Duplicated atribute in OTI:\n  %s" % line)
                        pass
                    # in both cases, as of 20.12.2019 00:55:12:
                    oti_gly[gly][linem.group(2)] = linem.group(3)
            else:
                log_lib.warning("Unrecognized line in OTI:\n  %s" % line)
        else: 
            log_lib.warning("Unrecognized line in OTI:\n  %s" % line)
    foti.close()
    oti = {'font': oti_fnt, 'glyphs': oti_gly, 'list': gly_lst}
    return oti

