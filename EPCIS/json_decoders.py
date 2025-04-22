from EPCIS.events import EPCISDocument, AssociationEvent, ObjectEvent, TransformationEvent, AggregationEvent, \
    EPCISExtension, Source, Destination, BusinessTransaction, QuantityElement
from EPCIS.masterdata import LocationNode, ProductNode


def convert_destination_list(destination):
    destination_list = []
    for item in destination:
        destination_list.append(Destination(item['type'], item['destination']))
    return destination_list


def convert_source_list(source):
    source_list = []
    for item in source:
        source_list.append(Source(item['type'], item['source']))
    return source_list

def convert_bizTransaction_list(bizTransaction):
    bizTransaction_list = []
    for item in bizTransaction:
        bizTransaction_list.append(BusinessTransaction(item['type'], item['bizTransaction']))
    return bizTransaction_list

def convert_quantity_list(quantity):
    quantity_list = []
    for item in quantity:
        quantity_list.append(QuantityElement(item['epcClass'], item['quantity'], item['uom']))
    return quantity_list


class EPCISEventConverter(object):
    def convert(self, data):
        event_id = data['eventID'].replace("ni:///sha-256;", "").replace("?ver=CBV2.0", "")
        if data['type'] == "ObjectEvent":
            event =  ObjectEvent(data['eventTime'], data['eventTimeZoneOffset'], data['recordTime'], data['action'], event_id=event_id)
        elif data['type'] == "TransformationEvent":
            event = TransformationEvent(data['eventTime'], data['eventTimeZoneOffset'], data['recordTime'], event_id=event_id)
        elif data['type'] == "AssociationEvent":
            event = AssociationEvent(data['eventTime'], data['eventTimeZoneOffset'], data['recordTime'], data['action'], event_id=event_id)
        elif data['type'] == "AggregationEvent":
            event = AggregationEvent(data['eventTime'], data['eventTimeZoneOffset'], data['recordTime'], data['action'], event_id=event_id)

        if "bizStep" in data:
            event.biz_step = data['bizStep']
        if "disposition" in data:
            event.disposition = data['disposition']
        if "readPoint" in data:
            event.read_point = data['readPoint']['id']
        if "bizLocation" in data:
            event.biz_location = data['bizLocation']['id']
        if "sourceList" in data:
            event.source_list = convert_source_list(data['sourceList'])
        if "destinationList" in data:
            event.destination_list = convert_destination_list(data['destinationList'])
        if "bizTransactionList" in data:
            event.biz_bizTransaction_list = convert_bizTransaction_list(data['bizTransactionList'])

        for key in data:
            if len(key.split(":")) == 2:
                namespace, name = key.split(":")
                extension = EPCISExtension(namespace, name, data[key])
                event.extension_collection.add_extension(extension)

        return event


class ObjectEventConverter(EPCISEventConverter):
    def convert(self, data):
        event = super(ObjectEventConverter, self).convert(data)
        if "epcList" in data:
            event.epc_list = data['epcList']
        if "quantityList" in data:
            event.quantity_list = convert_quantity_list(data['quantityList'])
        if "ilmd" in data:
            # TO DO: convert ilmd
            pass
        return event


class TransformationEventConverter(EPCISEventConverter):
    def convert(self, data):
        event = super(TransformationEventConverter, self).convert(data)
        if "inputEPCList" in data:
            event.epc_list = data['inputEPCList']
        if "outputEPCList" in data:
            event.epc_list = data['outputEPCList']
        if "inputQuantityList" in data:
            event.input_quantity_list = convert_quantity_list(data['inputQuantityList'])
        if "outputQuantityList" in data:
            event.output_quantity_list = convert_quantity_list(data['outputQuantityList'])
        if "transformationId" in data:
            event.transformation_id = data['transformationId']
        if "ilmd" in data:
            # TO DO: convert ilmd
            pass
        return event


class AggregationEventEncoder(EPCISEventConverter):
    def convert(self, data):
        event = super(AggregationEventEncoder, self).convert(data)
        if "parentID" in data:
            event.parent_id = data['parentID']
        if "childEPCs" in data:
            event.child_epcs = data['childEPCs']
        if "childQuantityList" in data:
            event.child_quantity_list = convert_quantity_list(data['childQuantityList'])
        return event


class EPCISJSONConverter(object):
    def convert(self, data):
        epcis = EPCISDocument()
        event_list = []
        if len(data['@context']) >= 2:
            for i in range(1, len(data['@context'])):
                for key, value in data['@context'][i].items():
                    if isinstance(value, str):
                        epcis.add_namespaces(key, value)

        if data['type'] == "EPCISDocument":
            masterdata_list = data['epcisHeader']['epcisMasterData']['vocabularyList']
            for item in masterdata_list:
                if item['type'] == 'urn:epcglobal:epcis:vtype:Location':
                    for location in item['vocabularyElementList']:
                        location = LocationNode.from_json(location)
                        epcis.add_location_masterdata(location)
                elif item['type'] == 'urn:epcglobal:epcis:vtype:EPCClass':
                    for product in item['vocabularyElementList']:
                        product = ProductNode.from_json(product)
                        epcis.add_product_masterdata(product)

            event_list = data['epcisBody']['eventList']

        elif data['type'] == "EPCISQueryDocument":
            event_list = data['epcisBody']['queryResults']['resultsBody']['eventList']

        for item in event_list:
            if item['type'] == "ObjectEvent":
                event = ObjectEventConverter().convert(item)
            elif item['type'] == "TransformationEvent":
                event = TransformationEventConverter().convert(item)
            elif item['type'] == "AssociationEvent":
                event = AggregationEventEncoder().convert(item)
            elif item['type'] == "AggregationEvent":
                event = AggregationEventEncoder().convert(item)
            epcis.add_event(event)
        return epcis
