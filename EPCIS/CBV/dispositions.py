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
# Copyright 2024 SerialLab Corp.  All rights reserved.

from enum import Enum


class Disposition(Enum):
    """
    CBV Disposition values as defined in section 7.2 of the standard.
    """

    active = "active"
    conformant = "conformant"
    container_closed = "container_closed"
    damaged = "damaged"
    destroyed = "destroyed"
    dispensed = "dispensed"
    disposed = "disposed"
    encoded = "encoded"
    expired = "expired"
    in_progress = "in_progress"
    in_transit = "in_transit"
    inactive = "inactive"
    needs_replacement = "needs_replacement"
    no_pedigree_match = "no_pedigree_match"
    non_sellable_other = "non_sellable_other"
    partially_dispensed = "partially_dispensed"
    recalled = "recalled"
    reserved = "reserved"
    retail_sold = "retail_sold"
    returned = "returned"
    sellable_accessible = "sellable_accessible"
    sellable_not_accessible = "sellable_not_accessible"
    stolen = "stolen"
    unavailable = "unavailable"
    unknown = "unknown"

    def __str__(self):
        return self.value
