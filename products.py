# vim: ai et sw=4 ts=4
import requests
import logging
import html
import xml.etree.ElementTree as ET
from datetime import datetime
import json


class Products:

    entryns = 'http://www.w3.org/2005/Atom'

    def __init__(self, url, username, password, product={}):
        self.url = url+'/Products'
        self.username = username
        self.password = password
        if product:
            self.load_xml(product)

    def load_xml(self, product={}):
        data = {
            '$filter': self._get_filter_from_product(product),
            '$orderby': 'IngestionDate desc',
            '$top': '1',
        }
        r = requests.get(self.url, auth=(self.username, self.password), params=data)
        self.xmltext = html.unescape(r.text)
        logging.debug(self.xmltext)
        try:
            self.xmlroot = ET.fromstring(self.xmltext)
        except:
            logging.critical(f'Error parsing xml document {self.url}')
            raise

    def _get_filter_from_product(self, product):
        if 'type' in product:
            return f"startswith(Name,'{product['type']}')"
        elif 'id' in product:
            return f"Id eq '{product['id']}'"
        elif 'filter' in product:
            return product['filter']

    def get_first_entry(self):
        return Entry(self.xmlroot.find(f'{{{self.entryns}}}entry'))
    
    def __repr__(self):
        return f'url:{self.url}'
        
class Entry:

    propsns = 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'
    datans = 'http://schemas.microsoft.com/ado/2007/08/dataservices'

    def __init__(self, xmlpart):
        self.xmlpart = xmlpart

    def get_id(self):
        eid = self.xmlpart.find(f'{{{self.propsns}}}properties/{{{self.datans}}}Id')
        return eid.text

    def get_ingestion_datetime(self):
        ig = self.xmlpart.find(f'{{{self.propsns}}}properties/{{{self.datans}}}IngestionDate')
        return datetime.fromisoformat(ig.text)

    def get_creation_datetime(self):
        ig = self.xmlpart.find(f'{{{self.propsns}}}properties/{{{self.datans}}}CreationDate')
        return datetime.fromisoformat(ig.text)

    def __repr__(self):
        return f'Id:{self.get_id()} IngestionDate:{self.get_ingestion_datetime()} CreationDate:{self.get_creation_datetime()}'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    with open('config.json') as file:
        config = json.load(file)

    local_products = Products(config['url'], config['username'], config['password'])
    local_products.load_xml({'type':'S3A'})
    e = local_products.get_first_entry()
    logging.info(local_products)
    logging.info(e)
