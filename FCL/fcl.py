import json

class FCLNode:
    def __init__(self, attributes):
        self.attributes = attributes

    def add_attribute(self, key, value):
        self.attributes[key] = value

    def get_output(self, property_list):
        node_output = []
        for key, value in self.attributes.items():
            if key in property_list:
                node_output.append({
                    'id': key,
                    'value': value
                })
        return node_output

class FCL:
    def __init__(self):
        self.version = "1.0.0"
        self.stations = {}
        self.deliveries = {}
        self.deliveries_rel = []
        self.settings = {}
        self.station_properties = {
            'ID': 'string',
            'Name': 'string',
            'Latitude': 'double',
            'Longitude': 'double'
        }
        self.deliveries_properties = {
            'ID': 'string',
            'from': 'string',
            'to': 'string'
        }
        self.deliveries_rel_properties = {
            'from': 'string',
            'to': 'string'
        }

    def add_station_properties(self, properties):
        self.station_properties.update(properties)

    def add_deliveries_properties(self, properties):
        self.deliveries_properties.update(properties)

    def add_station(self, id, name, lat, lon, attributes=None) -> FCLNode:
        node_attributes = {
            'ID': id,
            'Name': name,
            'Latitude': lat,
            'Longitude': lon
        }
        node_attributes.update(attributes or {})
        self.stations[id] = FCLNode(node_attributes)
        return self.stations[id]

    def add_delivery(self, id, from_id, to_id, attributes=None) -> FCLNode:
        node_attributes = {
            'ID': id,
            'from': from_id,
            'to': to_id
        }
        node_attributes.update(attributes or {})
        self.deliveries[id] = FCLNode(node_attributes)
        return self.deliveries[id]

    def add_deliveries_rel(self, from_id, to_id):
        node_attributes = {
            'from': from_id,
            'to': to_id
        }
        self.deliveries_rel.append(FCLNode(node_attributes))

    def get_station_id_set(self) -> set:
        return set(self.stations.keys())

    def generate_output(self):
        output = {
            'version': self.version,
            'data': {
                'version': self.version,
                'stations': {
                    'columnProperties': [],
                    'data': []
                },
                'deliveries': {
                    'columnProperties': [],
                    'data': []
                },
                'deliveryRelations': {
                    'columnProperties': [
                        {
                            "id": "from",
                            "type": "string"
                        },
                        {
                            "id": "to",
                            "type": "string"
                        }],
                    'data': []
                },

            }
        }
        station_output = output['data']['stations']
        deliveries_output = output['data']['deliveries']
        deliveries_rel_output = output['data']['deliveryRelations']

        for key, value in self.station_properties.items():
            station_output['columnProperties'].append(
                {
                    "id": key,
                    "type": value,
                }
            )

        for key, value in self.deliveries_properties.items():
            deliveries_output['columnProperties'].append(
                {
                    "id": key,
                    "type": value,
                }
            )

        for node in self.stations.values():
            station_output['data'].append(node.get_output(self.station_properties.keys()))

        for node in self.deliveries.values():
            deliveries_output['data'].append(node.get_output(self.deliveries_properties.keys()))

        for node in self.deliveries_rel:
            deliveries_rel_output['data'].append(node.get_output(['from', 'to']))

        return output
