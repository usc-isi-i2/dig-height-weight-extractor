# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-22 17:52:30
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-11-08 18:27:24

import re

######################################################################
#   Constant
######################################################################

# Constants for height
HW_HEIGHT_UNIT_METER = 'meter'
HW_HEIGHT_UNIT_CENTIMETER = 'centimeter'
HW_HEIGHT_UNIT_FOOT = 'foot'
HW_HEIGHT_UNIT_INCH = 'inch'

HW_HEIGHT_UNIT_CENTIMETER_ABBRS = ['cm']
HW_HEIGHT_UNIT_FOOT_ABBRS = ['ft']
HW_HEIGHT_UNIT_INCH_ABBRS = ['in']

HW_HEIGHT_UNITS_DICT = {
    HW_HEIGHT_UNIT_CENTIMETER: HW_HEIGHT_UNIT_CENTIMETER_ABBRS,
    HW_HEIGHT_UNIT_FOOT: HW_HEIGHT_UNIT_FOOT_ABBRS,
    HW_HEIGHT_UNIT_INCH: HW_HEIGHT_UNIT_INCH_ABBRS
}

# Constants for weight
HW_WEIGHT_UNIT_POUND = 'pound'
HW_WEIGHT_UNIT_KILOGRAM = 'kilogram'

HW_WEIGHT_UNIT_POUND_ABBRS = ['lb', 'lbs']
HW_WEIGHT_UNIT_KILOGRAM_ABBRS = ['kg']

HW_HEIGHT_UNITS_DICT = {
    HW_WEIGHT_UNIT_POUND: HW_WEIGHT_UNIT_POUND_ABBRS,
    HW_WEIGHT_UNIT_KILOGRAM: HW_WEIGHT_UNIT_KILOGRAM_ABBRS
}


######################################################################
#   Regular Expression
######################################################################

# Reg for target with unit, 'us': unit solution
reg_us_height_symbol = r'(?:\b\d\'{1,2}[ ]*\d{1,2}\b)'

reg_us_height_unit_cm = r'(?:\b\d{3}[ ]*cm\b)'
reg_us_height_unit_ft = r'(?:(?:\b\d{1}\.\d{1}[ ]*ft)|(?:\b\d{1}[ ]*ft))[ ]*(?:(?:\d{1}in\b)?|\b)'

reg_us_weight_unit_lb = r'\b\d{2,3}[ ]*(?:lb|lbs)\b'
reg_us_weight_unit_kg = r'\b\d{2}[ ]*kg\b'

re_us_height = re.compile(r'(?:' + r'|'.join([
    reg_us_height_symbol,
    reg_us_height_unit_cm,
    reg_us_height_unit_ft
]) + r')', re.IGNORECASE)

re_us_weight = re.compile(r'(?:' + r'|'.join([
    reg_us_weight_unit_lb,
    reg_us_weight_unit_kg
]) + r')', re.IGNORECASE)

# Reg for target after label height or weight, 'ls': label solution
reg_ls_height = r'(?<=height)[: \n]*' + r'(?:' + r'|'.join([
    reg_us_height_unit_cm,
    reg_us_height_unit_ft,
    reg_us_height_symbol,
    r'(?:\d{1}\.\d{1,2})',
    r'(?:\d{1,3})'
]) + r')'

reg_ls_weight = r'(?<=weight)[: \n]*' + r'(?:' + r'|'.join([
    reg_us_weight_unit_lb,
    reg_us_weight_unit_kg,
    r'(?:\d{1,3})'
]) + r')'

re_ls_height = re.compile(reg_ls_height, re.IGNORECASE)
re_ls_weight = re.compile(reg_ls_weight, re.IGNORECASE)

######################################################################
#   Main Class
######################################################################


class HWHelper(object):

    def extract_height(self, text):
        return re_us_height.findall(text) + re_ls_height.findall(text)

    def extract_weight(self, text):
        return re_us_weight.findall(text) + re_ls_weight.findall(text)

    def clean_extraction(self, extraction):
        extraction = extraction.replace(':', '')
        extraction = extraction.lower().strip()
        return extraction

    def normalize_height(self, extraction):
        extraction = self.clean_extraction(extraction)
        ans = {}
        if '\'' in extraction:
            # remove duplicate '
            extraction = '\''.join([_ for _ in extraction.split('\'') if _])
            extraction = extraction.strip('\'')  # remove following '

            feet, inch = extraction.split('\'', 1)
            ans[HW_HEIGHT_UNIT_FOOT] = int(feet)
            ans[HW_HEIGHT_UNIT_INCH] = int(inch)
        elif 'cm' in extraction:
            value, remaining = extraction.split('cm')
            ans[HW_HEIGHT_UNIT_CENTIMETER] = int(value.strip())
        elif 'ft' in extraction:
            value, remaining = extraction.split('ft')
            ans[HW_HEIGHT_UNIT_FOOT] = float(value.strip())
            if remaining:
                if remaining.isdigit():
                    ans[HW_HEIGHT_UNIT_INCH] = int(remaining)
                elif 'in' in remaining:
                    value, _ = remaining.split('in')
                    ans[HW_HEIGHT_UNIT_INCH] = int(value.strip())
                else:
                    print 'WARNING: contain uncatched case:', extraction
        elif '.' in extraction:
            meter, centimeter = extraction.split('.')
            ans[HW_HEIGHT_UNIT_METER] = int(meter)
            ans[HW_HEIGHT_UNIT_CENTIMETER] = int(centimeter.strip())
        elif extraction.isdigit():
            ans[HW_HEIGHT_UNIT_CENTIMETER] = int(extraction)

        return ans

    def normalize_weight(self, extraction):
        extraction = self.clean_extraction(extraction)
        ans = {}
        if 'lb' in extraction:
            value, remaining = extraction.split('lb')
            ans[HW_WEIGHT_UNIT_POUND] = int(value.strip())
        elif 'kg' in extraction:
            value, remaining = extraction.split('kg')
            ans[HW_WEIGHT_UNIT_KILOGRAM] = int(value.strip())
        elif extraction.isdigit():
            if len(extraction) == 2:
                ans[HW_WEIGHT_UNIT_KILOGRAM] = int(extraction)
            elif len(extraction) == 3:
                ans[HW_WEIGHT_UNIT_POUND] = int(extraction)
            else:
                print 'WARNING: contain uncatched case:', extraction

        return ans

    def remove_dups(self, extractions):
        return [dict(_) for _ in set([tuple(dict_item.items()) for dict_item in extractions if dict_item])]

    def extract(self, text):
        height_extractions = self.extract_height(text)
        weight_extractions = self.extract_weight(text)

        height_extractions = self.remove_dups(
            [self.normalize_height(_) for _ in height_extractions])
        weight_extractions = self.remove_dups(
            [self.normalize_weight(_) for _ in weight_extractions])

        return {
            'height': height_extractions,
            'weight': weight_extractions
        }


if __name__ == '__main__':
    # text = "\n TS RUBI: THE NAME SAYS IT ALL!  \n INCALL $250 OUTCALL $350 \n \n \n \n \n \n Gender \n Age \n Ethnicity \n Hair Color \n Eye Color \n Height \n Weight \n Measurements \n Affiliation \n Availability \n Available To \n \n \n \n \n Transsexual \n 27 \n Latino/Hispanic \n Brown \n Hazel \n 5'5\" \n 130 lb \n 34C - 28\" - 34\" \n "

    # text = "\n \n Height: \r\n                          5'3''\r\n                       \n \n \n \n \n \n Weight: \r\n                          125 lbs\r\n                       \n \n \n \n \n \n"

    # text = "Breasts DD Eyes gray Height 1.52 Skin Tanned Weight 60"
    # text = "I am 25 of age, stand 5ft5in, fair in complexion, Long hair"

    # text = "Measurements: 105lbs 5'2\" 34c with a beautiful face"

    text = "Travel: \n worldwide \n \n \n Weight: \n 117 lb (53 kg) \n \n \n Height: \n 5.5 ft (166 cm) \n \n \n Ethnicity: \n Indian \n"

    hw = HWHelper()
    print hw.extract(text)
