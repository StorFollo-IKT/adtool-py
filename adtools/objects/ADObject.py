from datetime import datetime

from adtools import ADTools, utils


class ADObject:
    adtools: ADTools
    dn = ''
    element: dict

    def __init__(self, adtools: ADTools, response):
        self.adtools = adtools

        if type(response) == dict and 'dn' in response:
            self.element = response
        elif type(response) == list and type(response[0]) == dict and 'dn' in response[0]:
            self.element = response[0]
        else:
            raise ValueError('Invalid response')

        self.dn = utils.uppercase_dn(self.element['dn'])

    def __getitem__(self, key):
        if key == 'dn':
            return self.dn
        if key == 'attributes':
            return self.element['attributes']

        return self.element['attributes'][key]

    def attributes(self):
        return self.element['attributes']

    def string(self, field) -> str:
        try:
            data = self[field]
            if data:
                return data.decode('utf-8')
        except UnicodeDecodeError as e:
            print('Error decoding field %s' % field)
            raise e

    def numeric(self, field) -> int:
        """
        Get numeric attribute
        :param field: Attribute name
        :return: Attribute value
        """
        try:
            data = self[field]
            if data:
                return int(data)
        except ValueError as e:
            print('Error decoding field %s' % field)
            raise e

    def bytes_int(self, field) -> int:
        if field in self.element:
            return int.from_bytes(self[field], 'big')

    def bytes(self, field) -> bytes:
        if field in self.element:
            return self[field]

    def hex(self, field) -> int:
        if field in self.element:
            return int(self[field], 16)

    def date(self, field) -> datetime:
        from ad_import.utils.ad_utils import parse_date
        data = self.numeric(field)
        if data:
            return parse_date(data)

    def date_string(self, field) -> datetime:
        data = self.string(field)
        # 2020 09 09 08:56:44.0Z
        if data:
            return datetime.strptime(data, '%Y%m%d%H%M%S.0Z')
