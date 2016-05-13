import xml.etree.ElementTree as ET


class DataWrapper:
    def __init__(self, source=None):
        self.map = {}
        self.list = []
        self.name = None
        if source:
            root = ET.parse(source).getroot()
            values = root.findall("./list/item/value")
            for v in values:
                self.list.append(v.text)
            values = root.findall("./mapProperty/item")
            for item in values:
                key = item.findtext("./key")
                value = item.findtext("./value")
                self.map[key] = value
            self.name = root.findtext("./name")

    def __bytes__(self):
        root = ET.Element('dataWrapper', {'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                                          'xmlns:xs': "http://www.w3.org/2001/XMLSchema"})
        root.append(self.list_to_xml())
        root.append(self.map_to_xml())
        if self.name:
            ET.SubElement(root, 'name').text = self.name

        return ET.tostring(root, encoding='utf-8')

    def list_to_xml(self):
        list_xml = ET.Element('list')
        for l in self.list:
            ET.SubElement(list_xml, 'value', {'xsi:type': self.get_xsi_type(l)}).text = l
        return list_xml

    def map_to_xml(self):
        map_xml = ET.Element('mapProperty')
        for k, v in self.map.items():
            item = ET.SubElement(map_xml, 'item')
            ET.SubElement(item, 'key').text = k
            ET.SubElement(item, 'value', {'xsi:type': self.get_xsi_type(v)}).text = v
        return map_xml

    @staticmethod
    def get_xsi_type(obj):
        if type(obj) is str:
            return 'xs:string'
        else:
            return ''