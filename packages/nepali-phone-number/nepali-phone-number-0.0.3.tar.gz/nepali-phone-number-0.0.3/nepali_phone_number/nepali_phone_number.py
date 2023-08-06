import re

from nepali_phone_number.config import config
from nepali_phone_number.datasets import nepali_english_digits, land_line_data, ncell_data
from nepali_phone_number.exceptions import (
    InvalidEnglishNumberException,
    InvalidNepaliNumberException,
    InvalidLandLineNumberException,
    InvalidPhoneNumberException
)
from nepali_phone_number.validators import is_english_number, is_nepali_number
from nepali_phone_number.regexs import (
    ncell_phone_number_regex,
    ntc_phone_number_regex,
    sky_phone_number_regex,
    utl_phone_number_regex,
    hello_phone_number_regex,
    smart_cell_phone_number_regex,
    phone_number_regex,
    land_line_number_regex,
    kathmandu_land_line_number_regex
)


class CommonClass:
    def __init__(self, nepali_number_input=None, english_number_input=None):

        if not nepali_number_input and not english_number_input:
            raise ValueError('At least one params required.')
        if nepali_number_input and english_number_input:
            raise ValueError('Only one param is allowed.')

        self._nepali_number = nepali_number_input
        self._english_number = english_number_input

        self._validate_inputs()

    def _validate_inputs(self):
        if self._english_number:
            if is_english_number(number=str(self._english_number)):
                self._english_number = str(self._english_number)
            else:
                raise InvalidEnglishNumberException()
        else:
            if is_nepali_number(number=str(self._nepali_number)):
                self._nepali_number = str(self._nepali_number)
            else:
                raise InvalidNepaliNumberException()

    def convert_to_nepali(self):
        if self._nepali_number:
            raise ValueError('With english_input_number, convert_to_nepali() can\'t be called.')

        converted_number = ''
        for n in self._english_number:
            for index in nepali_english_digits:
                if n.encode(encoding=config['encoding']) == index['english']:
                    converted_number += index['nepali'].decode(encoding=config['encoding'])
        return converted_number

    def convert_to_english(self):
        if self._english_number:
            raise ValueError('With english_input_number, convert_to_english() can\'t be called.')

        converted_number = ''
        for n in self._nepali_number:
            for index in nepali_english_digits:
                if n.encode(encoding=config['encoding']) == index['nepali']:
                    converted_number += index['english'].decode(encoding=config['encoding'])
        return converted_number

    def get_number_detail(self):
        raise NotImplementedError('get_number_detail() should be overridden.')

    def is_valid_number(self):
        raise NotImplementedError('is_valid_number() should be overridden.')


class PhoneNumberDetail:
    def __init__(self, number: str):
        self._number = number

    def get_detail(self):
        network_provider = self._get_network_provider()
        if network_provider == 'NCELL':
            extra_data = self._get_ncell_data()
            return {
                'number': self._number,
                'network_provider': network_provider,
                'zone': extra_data['zone'],
                'sim_type': extra_data['sim_type']
            }
        return {
            'number': self._number,
            'network_provider': network_provider
        }

    def _get_network_provider(self):
        if ncell_phone_number_regex.match(self._number):
            return 'NCELL'
        elif ntc_phone_number_regex.match(self._number):
            return 'NTC'
        elif sky_phone_number_regex.match(self._number):
            return 'SKY'
        elif utl_phone_number_regex.match(self._number):
            return 'UTL'
        elif hello_phone_number_regex.match(self._number):
            return 'HELLO'
        elif smart_cell_phone_number_regex.match(self._number):
            return 'SMART CELL'
        else:
            raise InvalidPhoneNumberException('Invalid Phone Number.')

    def _get_ncell_data(self):
        zone = ''
        sim_type = ''
        regexs = []

        for d in ncell_data:
            prepaid_code = ''
            pro_code = ''

            for code in d['prepaid']:
                prepaid_code += code + '|'

            for code in d['pro']:
                pro_code += code + '|'

            regexs.append(
                {
                    'zone': d['zone'],
                    'prepaid_regex': re.compile('^({})\d+$'.format(prepaid_code.rstrip('|'))),
                    'pro_regex': re.compile('^({})\d+$'.format(pro_code.rstrip('|')))
                }
            )

        for regex in regexs:
            if regex['pro_regex'].match(self._number):
                zone = regex['zone']
                sim_type = 'Pro'
                break
            else:
                if regex['prepaid_regex'].match(self._number):
                    zone = regex['zone']
                    sim_type = 'Prepaid'
                    break

        return {
            'zone': zone,
            'sim_type': sim_type
        }


class LandLineNumberDetail:
    def __init__(self, number: str):
        self._number = number

    def get_detail(self):
        return {
            'number': self._number,
            'area': self._get_area()
        }

    def _get_area(self):
        area_code = self._number[:3]
        if area_code in land_line_data:
            return land_line_data.get(area_code)
        else:
            area_code = self._number[:2]
            if area_code in land_line_data:
                return land_line_data.get(area_code)
        raise InvalidLandLineNumberException('Invalid LandLine Number.')


class NepaliPhoneNumber(CommonClass):
    """
    Class For Nepali Number
    """
    def get_number_detail(self):
        if self._english_number:
            number = self._english_number
        else:
            number = self.convert_to_english()
        if self.is_valid_number():
            return PhoneNumberDetail(number=number).get_detail()
        raise InvalidPhoneNumberException('Invalid Phone Number.')

    def is_valid_number(self):
        if self._english_number:
            number = self._english_number
        else:
            number = self.convert_to_english()

        if phone_number_regex.match(number):
            return True
        return False


class NepaliLandLineNumber(CommonClass):
    def get_number_detail(self):
        if self._english_number:
            number = self._english_number
        else:
            number = self.convert_to_english()

        if self.is_valid_number():
            return LandLineNumberDetail(number=number).get_detail()
        raise InvalidLandLineNumberException('Invalid LandLine Number.')

    def is_valid_number(self):
        if self._english_number:
            number = self._english_number
        else:
            number = self.convert_to_english()

        if kathmandu_land_line_number_regex.match(number):
            return True
        else:
            if land_line_number_regex.match(number):
                return True
            return False
