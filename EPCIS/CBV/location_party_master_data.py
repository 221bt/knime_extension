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
# Copyright 2018 Rob Magee,  All rights reserved.
'''
This section contains enumerations and classes taht
express master data attributes that may be used to describe
a physical location identifier or party identifier. Physical location master
data attributes may be used to describe a location identifier whether the
location identifier is used as a EPCIS Read Point, Business Location, Source,
or Destination. Party master data attributes may be used whether the party
identifier is used as an EPCIS Source or Destination.

Defined in section 10 of the CBV standard.
'''

from enum import Enum


class LocationEnum(Enum):
    def __str__(self):
        return self.value


class LocationPartyMasterDataAttributes(LocationEnum):
    '''
     As defined in section 10.2
    '''
    site = 'urn:epcglobal:cbv:mda:site'
    sst = 'urn:epcglobal:cbv:mda:sst'
    ssa = 'urn:epcglobal:cbv:mda:ssa'
    ssd = 'urn:epcglobal:cbv:mda:ssd'
    name = 'urn:epcglobal:cbv:mda:name'
    streetAddressOne = 'urn:epcglobal:cbv:mda:streetAddressOne'
    streetAddressTwo = 'urn:epcglobal:cbv:mda:streetAddressTwo'
    streetAddressThree = 'urn:epcglobal:cbv:mda:streetAddressThree'
    city = 'urn:epcglobal:cbv:mda:city'
    state = 'urn:epcglobal:cbv:mda:state'
    postalCode = 'urn:epcglobal:cbv:mda:postalCode'
    countryCode = 'urn:epcglobal:cbv:mda:countryCode'
    geoLocation = 'urn:epcglobal:cbv:mda:geoLocation'


class SubSiteTypeMmasterDataAttribute(LocationEnum):
    '''
     As defined in section 10.3.1
    '''
    backroom = '201'
    storage_area = '202'
    sales_floor = '203'
    returns_area = '207'
    production_area = '208'
    receiving_area = '209'
    shipping_area = '210'
    sales_floor_transition_area = '211'
    customer_pick_up_area = '212'
    yard = '213'
    container_deck = '214'
    cargo_terminal = '215'
    packaging_area = '251'
    picking_area = '252'
    pharmacy_area = '253'
    undefined = '299'


class SubSiteAttributesMasterDataAttribute(LocationEnum):
    '''
     As defined in section 10.3.2
    '''
    electronics = '401'
    cold_storage = '402'
    shelf = '403'
    frozen = '404'
    fresh = '405'
    promotion = '406'
    end_cap = '407'
    point_of_sale = '408'
    security = '409'
    general_mdse = '411'
    grocery = '412'
    box_crusher = '413'
    dock_door = '414'
    conveyor_belt = '415'
    pallet_wrapper = '416'
    fixed_reader = '417'
    mobile_reader = '418'
    shelf_storage = '419'
    returns = '420'
    staging = '421'
    assembly = '422'
    lay_away = '423'
    dispenser = '424'
    quarantine = '425'
    controlled_substance = '426'
    recalled_product = '427'
    quality_control = '428'
    printing_room = '429'
    loading_dock = '430'
    entrance_gate = '431'
    exit_gate = '432'
    gate = '433'
    read_point_verification_spot = '434'
