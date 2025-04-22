# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 Rob Magee.  All rights reserved.
import json
import re
import gettext
from datetime import datetime, timezone

_ = gettext.gettext


gs1_key_regex = {
    '00': r'^(\d{18})$',
    '01': r'^(\d{14})$',
    '253': r'^(\d{13})([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,17})$',
    '255': r'^(\d{13})(\d{0,12})$',
    '401': r'^([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,30})$',
    '402': r'^(\d{17})$',
    '414': r'^(\d{13})$',
    '417': r'^(\d{13})$',
    '8003': r'^(\d{14})([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,16})$',
    '8004': r'^([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,30})$',
    '8006': r'^(\d{14})(\d{2})(\d{2})$',
    '8010': r'^([\x23\x2D\x2F\x30-\x39\x41-\x5A]{0,30})$',
    '8017': r'^(\d{18})$',
    '8018': r'^(\d{18})$'
}

# Key starts with GCP
key_starts_with_gcp = {
    '00': False,
    '01': False,
    '253': True,
    '255': True,
    '401': True,
    '402': True,
    '414': True,
    '417': True,
    '8003': False,
    '8004': True,
    '8006': False,
    '8010': True,
    '8017': True,
    '8018': True
}


def get_iso_8601_regex():
    '''
    Returns a compiled ISO 8601 regex for use in validation of date strings.
    :return: A compiled regex.
    '''

    pattern = r'/(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+)|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d)|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d)/'
    return re.compile(pattern, re.VERBOSE)


def gtin_urn_generator(company_prefix, indicator, item_reference,
                       serial_numbers: list):
    '''
    A python generator that creates SGTIN URNs for the list of serial numbers
    passed in.

    :param company_prefix: The company prefix (GS1).
    :param indicator: The GS1 indicator digit for the GTIN
    :param item_reference: The item reference number for the GTIN
    :param serial_numbers: A list of serial numbers in string or integer format.
    :return: Generates a sgtin URN string for each serial number provided.
    '''
    prefix = 'urn:epc:id:sgtin:{0}.{1}{2}.'.format(company_prefix, indicator,
                                                   item_reference)
    if len(indicator) > 1:
        raise ValueError(_('The indicator may only be one digit in length.'))
    if len(company_prefix + indicator + item_reference) != 13:
        raise ValueError(_('The combined length of the company prefix,'
                           ' indicator digit and item reference number must'
                           ' be 13.'))
    for serial_number in serial_numbers:
        yield ''.join([prefix, str(serial_number)])


def sscc_urn_generator(company_prefix, extension, serial_numbers: list):
    '''
    A python generator that creates SSCC URNs for the list of serial numbers
    passed in.

    :param company_prefix: The company prefix (GS1).
    :param extension: The extension digit.
    :param serial_numbers: The serial reference numbers for the SSCC
    :return: Generates a SSCC URN string for each serial reference provided.
    '''
    sscc_length = 17
    prefix = 'urn:epc:id:sscc:{0}.{1}'.format(company_prefix, extension)

    for serial_number in serial_numbers:
        actual_length = len(company_prefix + extension + str(serial_number))
        if actual_length < sscc_length:
            padding = '0' * (sscc_length - actual_length)
        elif actual_length > sscc_length:
            raise ValueError(_('The combined length of the company prefix,'
                               ' extension digit and serial number'
                               ' must be 17 or less.'))
        else:
            padding = ''  # no padding by default.
        yield ''.join([prefix, padding, str(serial_number)])


def sgtin_url_generator(company_prefix, indicator, item_reference, extension=None, spliter='10'):
    if len(company_prefix + indicator + item_reference) != 13:
        raise ValueError(_('The combined length of the company prefix,'
                           ' indicator digit and item reference number must'
                           ' be 13.'))
    gtin = indicator+company_prefix+item_reference
    check_digit = calculate_check_digit(gtin)
    gs1_url = f'https://id.gs1.org/01/{gtin}{check_digit}'
    if extension is not None:
        gs1_url += f'/{spliter}/{extension}'
    return gs1_url


def sgln_url_geneartor(company_prefix, location_reference, extension='0'):
    gln = company_prefix+location_reference
    check_digit = calculate_check_digit(gln)
    gs1_url = f'https://id.gs1.org/414/{gln}{check_digit}/254/{extension}'
    return gs1_url


def gtin_to_urn(company_prefix, indicator, item_reference,
                serial_number: str):
    '''
    A python generator that creates SGTIN URNs for the list of serial numbers
    passed in.

    :param company_prefix: The company prefix (GS1).
    :param indicator: The GS1 indicator digit for the GTIN
    :param item_reference: The item reference number for the GTIN
    :param serial_number: A serial number.
    :return: Generates a sgtin URN string for each serial number provided.
    '''
    return 'urn:epc:id:sgtin:{0}.{1}{2}.{3}'.format(company_prefix, indicator,
                                                    item_reference,
                                                    serial_number)


def get_current_utc_time_and_offset():
    '''
    Based on the inbound datetime value, it will reuturn the ISO string
    and the ISO timezone offset value.  Helps when creating EPCIS events
    on the fly.

    :param datetime: The datetime instance you want to convert to a string.
    :return: A two-tuple with the datetime ISO string and the ISO timezone
        offset.
    '''
    val = datetime.now(timezone.utc).isoformat()
    return val, val[-6:]


def gln13_data_to_sgln_urn(company_prefix, location_reference, extension='0'):
    '''
    Takes the three parameters and outputs a compliant EPCGlobal urn.
    The company prefix and location reference must be a total of 12 digits-
    do not send in the check digit as part of the location reference.

    :param company_prefix: The company prefix
    :param location_reference: The location reference
    :param extension: The id of the sub-site for the GLN
    :return: An TDS 1.9 compliant SGLN URN value.
    '''

    if not (len(str(company_prefix) + str(location_reference)) == 12):
        raise ValueError(
            _('The company prefix and location reference variables'
              ' must total 12 digits in lenght when combined.'))
    return 'urn:epc:id:sgln:{0}.{1}.{2}'.format(company_prefix,
                                                location_reference,
                                                extension)


def get_gcp_length(a_i, gs1_key):
    try:
        # Check if GS1 Key complies with its corresponding RegEx
        if not re.match(gs1_key_regex[a_i], gs1_key):
            raise ValueError('The GS1 Key has an incorrect length or impermissible characters.')
    except KeyError:
        return "Invalid GS1 Key prefix."

    # Variables storing identified gcp length and specifying prefix length/search string
    gcp_length = ""
    j = 12
    gcp_dict = json.load(open('EPCIS/asset/gcpprefixformatlist.json', 'r', encoding="utf8"))['GCPPrefixFormatList']['entry']

    # Normalize leading zero so that function works consistently for all GS1 keys
    if key_starts_with_gcp[a_i]:
        gs1_key = '0' + gs1_key

    # Normalize further by removing any characters after a non-numeric character appears, if present
    first_non_numeric_index = next((i for i, c in enumerate(gs1_key) if not c.isdigit()), -1)
    if first_non_numeric_index != -1:
        gs1_key = gs1_key[:first_non_numeric_index]

    # Check if there are matching 12-digit prefix values.
    # If not, iterate further (i.e. decrease GCP length) until there is a match.
    # Then, return corresponding GCP Length Value
    while j > 2 and not gcp_length:
        for item in gcp_dict:
            if len(item['prefix']) == j and gs1_key[1:j+1] in item['prefix']:
                gcp_length = item['gcpLength']
                return gcp_length
        j -= 1

    if not gcp_length:
        raise ValueError('No matching value. Try Verified by GS1 (https://www.gs1.org/services/verified-by-gs1) or contact your local GS1 MO.')

    return gcp_length

def gs1_sgln_uri_to_urn(gs1_url):
    gs1_key, extension = gs1_url.split('/414/')[1].split('/254/')
    gcp_length = get_gcp_length('414', gs1_key)
    company_prefix, location_reference = gs1_key[:gcp_length], gs1_key[gcp_length:-1]
    return gln13_data_to_sgln_urn(company_prefix, location_reference, extension)


def calculate_check_digit(gtin):
    valid_digit_list = [3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]
    valid_digit_list.reverse()
    sum = 0

    for i in range(len(gtin)):
        sum += int(gtin[len(gtin) - i - 1]) * valid_digit_list[i]

    return (10 - sum % 10) % 10


