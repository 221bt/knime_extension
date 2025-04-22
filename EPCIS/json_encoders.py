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
from datetime import datetime
from json import JSONEncoder
from typing import List

from EPCIS import events

QList = List[events.QuantityElement]

import json


class JSONFormatMixin:
    """
    Provides formatting options for JSON output such as compression (stripping
    of white space) and pretty printing. Must be used on a class that already
    utilizes the `template_events.TemplateMixin`.
    """

    def render_pretty_json(self, indent=4, sort_keys=False):
        """
        Pretty prints the JSON output.
        :param indent: Default of 4.
        :param sort_keys: Default of False.
        :return: A formatted JSON string indented and (potentially) sorted.
        """
        return json.dumps(
            self.encoder.default(self), indent=indent, sort_keys=sort_keys
        )

    def render_json(self):
        """
        Will strip all white space from the template output.
        :return: A JSON string with no whitespace.
        """
        return self.encoder.encode(self)

    def render_dict(self):
        """
        Will return the python dictionary rendered by the JSON encoder.
        :return: A dictionary.
        """
        return self.encoder.default(self)


class SourceListJSONEncoder(JSONEncoder):
    def default(self, o):
        return {o.type: o.source}


class QuantityMixin:
    def get_quantity_list(self, list: QList):
        if list:
            ret = [
                {"epcClass": item.epc_class, "quantity": item.quantity, "uom": item.uom}
                for item in list
            ]
        else:
            ret = []
        return ret


class DateHelperMixin:
    """
    If a datetime object is supplied will convert to iso 8601 string,
    if not will just use the string
    """

    def get_date(self, value):
        return (
            value.isoformat(timespec='microseconds')
            if isinstance(value, datetime)
            else value
        )


class ErrorDeclarationMixin:
    """
    Handles encoding the error declarations for encoders that require this.
    """

    def get_error_declaration(self, error_declaration: events.ErrorDeclaration):
        if error_declaration:
            return {
                "declarationTime": error_declaration.declaration_time,
                "reason": error_declaration.reason,
                "correctiveEventIDs": [
                    id for id in error_declaration.corrective_event_ids
                ],
            }


class ListMixin:
    """
    Handles the source destination BT and ILMD lists for encoders that
    require these.
    """

    def get_source_list(self, source_list):
        """
        Return the encoded list if it is not none or an empty dictionary.
        :param o:
        :return: A dictionary of source values.
        """
        ret = [{
            "type": item.type,
            "source": item.source
        } for item in source_list]
        return ret

    def get_destination_list(self, destination_list):
        """
        Return the encoded list if it is not none or an empty dictionary.
        :param o:
        :return: A dictionary of destination values.
        """
        ret = [{
            "type": item.type,
            "destination": item.destination
        } for item in destination_list]

        return ret

    def get_business_transaction_list(self, business_transaction_list):
        """
        Return the encoded list if it is not none or an empty dictionary.
        :param o:
        :return: A dictionary of BT values.
        """
        ret = [{
            "type": str(bt.type),
            "bizTransaction": str(bt.biz_transaction)
        } for bt in business_transaction_list]

        return ret

    def get_ilmd_list(self, ilmd):
        """
        Return the encoded list if it is not none or an empty dictionary.
        :param o:
        :return: A dictionary of ILMD values.
        """
        ret = {str(item.name): item.value for item in ilmd}

        return ret


class EPCISEventEncoder(
    JSONEncoder, ErrorDeclarationMixin, QuantityMixin, DateHelperMixin
):
    """
    All EPCIS classes share these common elements.  This is the base
    encoder.
    """

    def default(self, o: events.EPCISEvent):
        record_time = self.get_date(o.record_time) if o.record_time else None
        ret = {
            "type": o.type,
            "eventTime": self.get_date(o.event_time) + o.event_timezone_offset,
            "eventTimeZoneOffset": o.event_timezone_offset,
            "recordTime": record_time + o.event_timezone_offset
        }
        if o.event_id:
            ret["eventID"] = "ni:///sha-256;{}?ver=CBV2.0".format(o.event_id)
        if o.error_declaration:
            ret["errorDeclaration"] = self.get_error_declaration(o.error_declaration)
        for extension in o.extension_collection.extensions.values():
            ret[extension.epcis_key] = extension.content
        return ret


class EPCISBusinessEventEncoder(EPCISEventEncoder, ListMixin):
    """
    These elements are shared by the object, aggregation and transaction
    event classes- this is the base for those.
    """

    def default(self, o):
        """
        Creates default set of fields for object, transaction and
        aggregation events.
        :param o: The event to create the default set of fields for.
        :return: An EPCPyYes.core.v1_2.events.EPCISBusinessEvent instance.
        """
        if isinstance(o, events.EPCISBusinessEvent):
            ret = super(EPCISBusinessEventEncoder, self).default(o)
            if o.action:
                ret["action"] = o.action
            if o.biz_step:
                ret["bizStep"] = o.biz_step
            if o.disposition:
                ret["disposition"] = o.disposition
            if o.read_point:
                ret["readPoint"] = {
                    "id": o.read_point
                }
            if o.biz_location:
                ret["bizLocation"] = {
                    "id": o.biz_location
                }
            if o.business_transaction_list:
                ret["bizTransactionList"] = self.get_business_transaction_list(o.business_transaction_list)
            if o.source_list:
                ret["sourceList"] = self.get_source_list(o.source_list)
            if o.destination_list:
                ret["destinationList"] = self.get_destination_list(o.destination_list)

            return ret


class ObjectEventEncoder(EPCISBusinessEventEncoder, ListMixin):
    """
    Encodes an `EPCPyYes.core.v1_2.template_events.ObjectEvent` to
    JSON.
    """

    def default(self, o):
        if isinstance(o, events.ObjectEvent):
            ret = super(ObjectEventEncoder, self).default(o)
            if o.epc_list:
                ret["epcList"] = [epc for epc in o.epc_list]
            if o.ilmd:
                ret["ilmd"] = o.ilmd
            if o.quantity_list:
                ret["quantityList"] = self.get_quantity_list(o.quantity_list)

            return ret


class AggregationEventEncoder(EPCISBusinessEventEncoder):
    """
    Encodes an `EPCPyYes.core.v1_2.template_events.AggregationEvent` to
    JSON.
    """

    def default(self, o: events.AggregationEvent | events.AssociationEvent):
        ret = super().default(o)
        if o.parent_id:
            ret["parentID"] = o.parent_id
        if o.child_epcs:
            ret["childEPCs"] = [epc for epc in o.child_epcs]
        if o.child_quantity_list:
            ret["childQuantityList"] = self.get_quantity_list(o.child_quantity_list)

        return ret


class TransactionEventEncoder(EPCISBusinessEventEncoder):
    """
    Encodes an `EPCPyYes.core.v1_2.template_events.TransactionEvent` to
    JSON.
    """

    def default(self, o: events.TransactionEvent):
        ret = super().default(o)
        if o.epc_list:
            ret["epcList"] = [epc for epc in o.epc_list]
        if o.parent_id:
            ret["parentId"] = o.parent_id
        if o.quantity_list:
            ret["quantityList"] = self.get_quantity_list(o.quantity_list)

        return ret


class TransformationEventEncoder(EPCISBusinessEventEncoder, ListMixin):
    """
    Encodes an `EPCPyYes.core.v1_2.template_events.TransformationEvent` to
    JSON.  This class can not inherit from the business base class due
    to its radically different structure and general purpose.
    """

    def default(self, o: events.TransformationEvent):
        ret = super().default(o)
        if o.input_epc_list:
            ret['inputEPCList'] = [epc for epc in o.input_epc_list]
        if o.input_quantity_list:
            ret['inputQuantityList'] = self.get_quantity_list(o.input_quantity_list)
        if o.output_epc_list:
            ret['outputEPCList'] = [epc for epc in o.output_epc_list]
        if o.output_quantity_list:
            ret['outputQuantityList'] = self.get_quantity_list(o.output_quantity_list)
        if o.transformation_id:
            ret['transformationId'] = o.transformation_id
        if o.ilmd:
            ret["ilmd"] = o.ilmd

        return ret


class EPCISDocumentEncoder(JSONEncoder, DateHelperMixin):
    def default(self, o: events.EPCISDocument, include_masterdata = True, include_events = True):
        ret = {
            "type": "EPCISDocument",
            "schemaVersion": "2.0",
            "creationDate": o.created_date,
            "epcisHeader": {
                "epcisMasterData": {
                    "vocabularyList": []
                }
            },
            "epcisBody": {
                "eventList": []
            },
            "@context": [
                "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld"
            ]
        }

        obj = ObjectEventEncoder()
        agg = AggregationEventEncoder()
        trans = TransformationEventEncoder()
        xact = TransactionEventEncoder()

        if include_masterdata:
            if o.product_masterdata:
                ret["epcisHeader"]["epcisMasterData"]["vocabularyList"].append({
                    "type": "urn:epcglobal:epcis:vtype:EPCClass",
                    "vocabularyElementList": [product_masterdata.to_epcis() for product_masterdata in o.product_masterdata.values()]
                })

            if o.location_masterdata:
                ret["epcisHeader"]["epcisMasterData"]["vocabularyList"].append({
                    "type": "urn:epcglobal:epcis:vtype:Location",
                    "vocabularyElementList": [location_masterdata.to_epcis() for location_masterdata in o.location_masterdata.values()]
                })

        if include_events:
            for event in o.events.values():
                if event.type == "ObjectEvent":
                    result = obj.default(event)
                elif event.type == "TransformationEvent":
                    result = trans.default(event)
                elif event.type == "AssociationEvent":
                    result = agg.default(event)
                elif event.type == "AggregationEvent":
                    result = agg.default(event)
                ret["epcisBody"]["eventList"].append(result)

        if o.namespaces:
            for key, value in o.namespaces.items():
                ret["@context"].append({
                    key: value
                })

        return ret

    def list_events(self, event_list, encoder):
        return [encoder.default(event) for event in event_list] or []

    def list_template_events(self, template_events):
        return [event.encoder.default(event) for event in template_events]
