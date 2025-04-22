class MasterDataNode:
    def __init__(self, id):
        self._id = id
        self.attributes = {}

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def to_json(self):
        result = {
            "isA": "VocabularyElement",
            "id": self._id,
        }
        return result

    def to_epcis(self):
        result = {
            'id': self.id,
            'attributes': []
        }

        for key, value in self.attributes.items():
            result['attributes'].append({
                "id": key,
                "attribute": value,
            })
        return result


class LocationNode(MasterDataNode):
    def __init__(self, id, name, address, city, state, zip, country, lat, lng):
        super().__init__(id)
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zip
        self.country = country
        self.lat = lat
        self.lng = lng

    @property
    def geo_id(self):
        return "geo:" + str(self.lat) + "," + str(self.lng)

    def to_json(self):
        result = MasterDataNode.to_json(self)
        result.update({
            "cbvmda:name": self.name,
            "cbvmda:streetAddressOne": self.address,
            "cbvmda:city": self.city,
            "cbvmda:state": self.state,
            "cbvmda:postalCode": self.zipcode,
            "cbvmda:countryCode": self.country,
            "cbvmda:geoLocation": self.geo_id
        })
        return result

    def to_epcis(self):
        self.attributes.update({
            "cbvmda:name": self.name,
            "cbvmda:streetAddressOne": self.address,
            "cbvmda:city": self.city,
            "cbvmda:state": self.state,
            "cbvmda:postalCode": self.zipcode,
            "cbvmda:countryCode": self.country,
            "cbvmda:geoLocation": self.geo_id
        })
        result = MasterDataNode.to_epcis(self)
        return result

    @classmethod
    def from_json(cls, data):
        name, address, city, state, zip, country, lat, lng = '', '', '', '', '', '', 0, 0
        attributes = {}
        for attribute in data["attributes"]:
            if attribute['id'].split(':')[-1] == 'name':
                name = attribute['attribute']
            elif attribute['id'].split(':')[-1] == 'streetAddressOne':
                address = attribute['attribute']
            elif attribute['id'].split(':')[-1] == 'city':
                city = attribute['attribute']
            elif attribute['id'].split(':')[-1] == 'state':
                state = attribute['attribute']
            elif attribute['id'].split(':')[-1] == 'postalCode':
                zip = attribute['attribute']
            elif attribute['id'].split(':')[-1] == 'countryCode':
                country = attribute['attribute']
            elif attribute['id'].split(':')[-1] == 'geoLocation':
                temp = attribute['attribute'].split(':')[-1].split(',')
                lat, lng = float(temp[0]), float(temp[1])
            else:
                attributes.update({attribute['id']: attribute['attribute']})
        node = cls(data['id'], name, address, city, state, zip, country, lat, lng)
        node.attributes.update(attributes)
        return node


class ProductNode(MasterDataNode):
    def __init__(self, id, name):
        super().__init__(id)
        self.name = name

    def to_json(self):
        result = MasterDataNode.to_json(self)
        result.update({
            "cbvmda:descriptionShort": self.name
        })
        return result

    def to_epcis(self):
        self.attributes.update({
            "cbvmda:descriptionShort": self.name
        })
        result = MasterDataNode.to_epcis(self)
        return result

    @classmethod
    def from_json(cls, data):
        name = ''
        for attribute in data["attributes"]:
            if attribute['id'].split(':')[-1] == 'descriptionShort':
                name = attribute['attribute']
        return cls(data['id'], name)
