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

from . import instance_lot_master_data
import gettext

_ = gettext.gettext


def make_trade_item_master_data_urn(company_prefix, indicator_digit,
                                    item_reference,
                                    lot=None, serial_number=None):
    '''
    Create the right trade item master data urn based on supplied values
    per the section 9 and 7.3.3.3.3 instructions in the standard.

    :param company_prefix: Company prefix.
    :param indicator_digit: Product indicator digit
    :param item_reference: The Item reference number.
    :param lot: (Optional) the lot number. If supplied, this will result in
        a lot-based identifier and the serial_number will be ignored.
    :param serial_number: (Optional) the serial number of the trade item.
    :return: A properly formatted trade item master data urn value.
    '''
    if len(company_prefix) + len(indicator_digit) + len(item_reference) > 13:
        raise ValueError(_('The length of the company_prefix, '
                           'indicator_digit and item_reference parameters '
                           'must be 13 digits when combined.'))
    if lot:
        urn = 'urn:epc:class:lgtin:{}.{}{}.{}'.format(
            company_prefix,
            indicator_digit,
            item_reference,
            lot)
    elif serial_number:
        urn = 'urn:epc:id:sgtin:{}.{}{}.{}'.format(
            company_prefix,
            indicator_digit,
            item_reference,
            serial_number)
    else:
        urn = 'urn:epc:idpat:sgtin:{}.{}{}.{}'.format(
            company_prefix,
            indicator_digit,
            item_reference,
            '*')
    return urn


def get_ilmd_enum_by_value(value: str):
    """
    Returns an enum in the ILMD module based on the inbound string value or
    None if no enum containing value is found.
    :param value: The value to search for.
    """
    for name, enum in instance_lot_master_data.__dict__.items():
        if 'Attribute' in name:
            try:
                enum = enum(value)
                return enum
            except (ValueError, TypeError):
                pass
    return None