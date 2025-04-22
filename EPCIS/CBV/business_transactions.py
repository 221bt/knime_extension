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

from enum import Enum


class BusinessTransactionType(Enum):
    '''
    Business Transaction Types as defined in section 7.3 of the standard.
    '''
    Bill_Of_Lading = 'bol'
    Despatch_Advice = 'desadv'
    Invoice = 'inv'
    Pedigree = 'pedigree'
    Purchase_Order = 'po'
    Purchase_Order_Confirmation = 'poc'
    Production_Order = 'prodorder'
    Receiving_Advice = 'recadv'
    Return_Merchandise_Authorization = 'rma'
    Test_Procedure = 'testprd'
    Test_Result = 'testres'
    Upstream_EPCIS_Event = 'upevt'

    def __str__(self):
        return self.value