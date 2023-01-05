# vim: ai et sw=4 ts=4
from products import Products
from dhusparser import DhusConfig
import logging
from datetime import timedelta
import sys
import json


class NagiosChecker:

    results = {}

    def __init__(self, local_products, warn, crit):
        self.local_products = local_products
        self.warn = warn
        self.crit = crit

    """
    Walks through all active synchronizers in dhus config file (dhus.xml)
    measuring creation date of last element in local repository
    """
    def check_dhus_config(self, dconfig):
        dhusconfig = DhusConfig(dconfig)
        for syn in dhusconfig.get_active_synchronizers():
            self.local_products.load_xml({'filter': syn.get_filter()})
            loc_entry = self.local_products.get_first_entry()
            logging.info(self.local_products)
            logging.info(loc_entry)
        
            syn_products = Products(syn.get_url(), syn.get_login(), syn.get_password(), {'id': loc_entry.get_id()})
            syn_entry = syn_products.get_first_entry()
            logging.info(syn_products)
            logging.info(syn_entry)

            self.results[syn.get_label()] = loc_entry.get_creation_datetime() - syn_entry.get_creation_datetime()

    def format_result_output(self):
        ecode = 0
        emsg = 'OK'
        msgs = []
        for stype, delta in self.results.items():
            if delta > self.crit:
                res = 'CRIT'
                ecode = 2
            elif delta > self.warn:
                res = 'WARN'
                if ecode == 0: ecode = 1
            else:
                res = 'OK'
            msgs.append('{} {}:[{}min]'.format(res, stype, int(delta.total_seconds()/60)))
        return (ecode, ', '.join(msgs))
                

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
	
    with open('config.json') as file:
        config = json.load(file)

    warn = timedelta(hours=6)
    crit = timedelta(hours=12)

    local_products = Products(config['url'], config['username'], config['password'])
    nag = NagiosChecker(local_products, warn, crit)
    
    # Possible products=(S1A S1B S2A S2B S3A S3B)
    # Check all dhus_configs
    for dconfig in config['dhus_configs']:
        nag.check_dhus_config(dconfig)

    # Get the results
    (ecode, msgs) = nag.format_result_output()
    print(msgs)
    sys.exit(ecode)
