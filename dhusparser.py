# vim: ai et sw=4 ts=4
import xml.etree.ElementTree as ET
import logging


class DhusConfig:
    
    namespace = 'fr.gael.dhus.database.object.config'

    def __init__(self, xmlfile):
        self.xmltree = ET.parse(xmlfile)
        self.xmlroot = self.xmltree.getroot()

    def get_active_synchronizers(self):
        filtered = []
        synchronizers = self.xmlroot.findall('./{{{0}}}synchronizers/'.format(self.namespace))
        for synchronizer in synchronizers:
            new_synch = Synchronizer(synchronizer)
            if new_synch.is_active():
                filtered.append(Synchronizer(synchronizer))
        return filtered


class Synchronizer:

    namespace = 'fr.gael.dhus.database.object.config.synchronizer'
    
    def __init__(self, xmlpart):
        self.xmlpart = xmlpart

    def get_label(self):
        return self.xmlpart.find('./{{{}}}label'.format(self.namespace)).text

    def get_url(self):
        return self.xmlpart.find('./{{{}}}serviceUrl'.format(self.namespace)).text

    def get_login(self):
        return self.xmlpart.find('./{{{}}}serviceLogin'.format(self.namespace)).text

    def get_password(self):
        return self.xmlpart.find('./{{{}}}servicePassword'.format(self.namespace)).text

    def is_active(self):
        return self.xmlpart.find('./{{{}}}active'.format(self.namespace)).text in ['True', 'true']

    def get_filter(self):
        return self.xmlpart.find('./{{{}}}filterParam'.format(self.namespace)).text

    def __repr__(self):
        return 'label:{} active:{}'.format(self.get_label(), self.is_active())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    dhusconfig = DhusConfig('dhus-be1.xml')
    logging.debug(dhusconfig.get_active_synchronizers())
