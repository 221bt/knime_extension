import json
import uuid
from collections import defaultdict

from EPCIS.events import EPCISDocument
from EPCIS.json_decoders import EPCISJSONConverter
from FCL.fcl import FCL


def build_event_relation(epcis, tracking_extension_name):
    aggregation_id = []
    for event in epcis.events.values():
        previous_id_extension = event.extension_collection.extensions.get(tracking_extension_name, None)
        if previous_id_extension:
            for parent_event_id in previous_id_extension.content:
                epcis.events[parent_event_id].children.append(event)

    for event in epcis.events.values():
        if event.type == 'AggregationEvent':
            previous_id_extension = event.extension_collection.extensions.get(tracking_extension_name, None)
            if previous_id_extension:
                for parent_event_id in previous_id_extension.content:
                    epcis.events[parent_event_id].children.extend(event.children)
            aggregation_id.append(event.event_id)

    for id in aggregation_id:
        del epcis.events[id]


def gtin_decoder(gtin):
    if gtin[:3] == 'urn':
        temp = gtin.split(':')[-1]
        product, lot = temp.lsplit('.', 1)
    else:
        temp = gtin.split('/01/')[1]
        if len(temp.split('/10/')) == 2:
            product, lot = temp.split('/10/')
        else:
            product, lot = temp, ''
    return product, lot


def convert_fcl_json(epcis: EPCISDocument):
    fcl = FCL()
    event_del_dict = defaultdict(list)
    event_relation = []
    fcl.add_station_properties({
        "Address": 'string',
        "Country": 'string',
        "Role": 'string'
    })
    fcl.add_deliveries_properties({
        "Name": 'string',
        "Lot ID": 'string',
        "Date Delivery Arrival": 'string',
        "Amount": 'string',
        "Event Type": 'string'
    })
    for business in epcis.location_masterdata.values():
        if business.id in fcl.get_station_id_set():
            continue

        station_node = fcl.add_station(business.id, business.name, float(business.lat), float(business.lng))
        station_node.add_attribute("Address", ",".join([business.address, business.city, business.state,
                                                        business.country]))
        for key in business.attributes:
            if key.split(':')[1] == 'role':
                station_node.add_attribute("Role", business.attributes[key])

    for event in epcis.events.values():
        for child in event.children:
            event_id = event.event_id
            from_location, to_location = event.biz_location, child.biz_location
            if event.type == 'TransformationEvent':
                quantity_list = event.output_quantity_list
            elif event.type == 'AssociationEvent' or event.type == 'AggregationEvent':
                quantity_list = event.child_quantity_list
            else:
                quantity_list = event.quantity_list
            for quantity_item in quantity_list:
                delivery_id = str(uuid.uuid4()).replace('-', '')
                event_del_dict[event_id].append(delivery_id)
                product_id, product_lot = gtin_decoder(quantity_item.epc_class)

                delivery_node = fcl.add_delivery(delivery_id, from_location, to_location)
                delivery_node.add_attribute("Name", product_id)
                delivery_node.add_attribute("Lot ID", product_lot)
                delivery_node.add_attribute("Date Delivery Arrival", event.event_time)
                delivery_node.add_attribute("Amount", str(quantity_item.quantity) + ' ' + quantity_item.uom)
                delivery_node.add_attribute("Event Type", event.type)

            if child.children:
                # fcl.add_deliveries_rel(delivery_id, child.id)
                event_relation.append([event.event_id, child.event_id])

    for event_id, child_id in event_relation:
        from_ids = event_del_dict[event_id]
        to_ids = event_del_dict[child_id]
        for from_id in from_ids:
            for to_id in to_ids:
                fcl.add_deliveries_rel(from_id, to_id)

    return fcl.generate_output()


def generate_fcl(data, tracking_extension_name):
    converter = EPCISJSONConverter()
    epcis = converter.convert(data)
    build_event_relation(epcis, tracking_extension_name)
    result = convert_fcl_json(epcis)
    return result
