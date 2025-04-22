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
'''
This section containes enumerations that specifie
master data attributes that may be used to describe
a trade item identifier that appears in the “what” dimension of an EPCIS event,
including the EPC, Parent ID, and EPC Class fields.

Defined in section 9 of the CBV standard.

'''
import gettext
from enum import Enum

from ..events import InstanceLotMasterDataAttribute

_ = gettext.gettext


class ILMDAttributeName(Enum):
    def __str__(self):
        return self.value


class TradeItemLevelAttributeName(ILMDAttributeName):
    '''
    The following attributes may be used to describe a trade
    item identifier at the trade item (GTIN) level.

    As defined in section 9.2.1
    '''
    additionalTradeItemIdentification = 'additionalTradeItemIdentification'
    additionalTradeItemIdentificationTypeCode = 'additionalTradeItemIdentificationTypeCode'
    countryOfOrigin = 'countryOfOrigin'
    descriptionShort = 'descriptionShort'
    dosageFormType = 'dosageFormType'
    drainedWeight = 'drainedWeight'
    functionalName = 'functionalName'
    grossWeight = 'grossWeight '
    manufacturerOfTradeItemPartyName = 'manufacturerOfTradeItemPartyName'
    netWeight = 'netWeight '
    labelDescription = 'labelDescription'
    regulatedProductName = 'regulatedProductName'
    strengthDescription = 'strengthDescription'
    tradeItemDescription = 'tradeItemDescription'


class LotLevelAttributeName(ILMDAttributeName):
    '''
    The following attributes may be used to describe a trade item
    identifier at the lot level.

    As defined in section 9.2.2
    '''
    bestBeforeDate = 'bestBeforeDate'
    countryOfOrigin = 'countryOfOrigin'
    farmList = 'farmList'
    firstFreezeDate = 'firstFreezeDate'
    growingMethodCode = 'growingMethodCode'
    harvestEndDate = 'harvestEndDate'
    harvestStartDate = 'harvestStartDate'
    itemExpirationDate = 'itemExpirationDate'
    sellByDate = 'sellByDate'
    storageStateCode = 'storageStateCode'


class ItemLevelAttributeName(ILMDAttributeName):
    '''
    The following attributes may be used to describe a trade item
    identifier at the trade item (GTIN) level.

    As defined in section 9.2.3
    '''
    countryOfOrigin = 'countryOfOrigin'
    drainedWeight = 'drainedWeight'
    grossWeight = 'grossWeight'
    lotNumber = 'lotNumber'
    netWeight = 'netWeight'
    measurement = 'measurement'
    measurementUnitCode = 'measurementUnitCode'


class FarmListAttributeName(ILMDAttributeName):
    farmIdentification = 'farmIdentification'
    farmIdentificationTypeCode = 'farmIdentificationTypeCode'


class MeasurementAttributeName(ILMDAttributeName):
    '''
    Each value of type Measurement is a structure having the
    subelements represented in this enumeration.

    As defined in seciton 9.2.4
    '''
    measurement = 'measurement'
    measurementUnitCode = 'measurementUnitCode'


class InstanceLotMasterDataAttribute(InstanceLotMasterDataAttribute):
    '''
    The ILMD class as defined in section 7.3.6 of the EPCIS
    standard and section 9 of the CBV.
    '''

    def __init__(self, name: str, value: str):
        '''
        Initializes a new InstanceLotMasterDataAttribute instance that
        is CBV 1.2 compliant.

        :param name: An ILMDAttribute as defined in the CBV
        :param value: The value of that attribute.
        '''
        self._value = value
        self._name = name

    @property
    def name(self):
        '''
        Gets and sets this class's :class:`~ILMDAttributeName` enum.

        :return: an :class:`~ILMDAttributeName` enum from the CBV instance_lot_master_data
            package.  Use the value attribute of the returned enum to convert
            to a string.
        '''
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
