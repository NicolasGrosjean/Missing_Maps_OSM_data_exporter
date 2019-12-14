import os
import unittest
import xml.etree.ElementTree as ET

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.extract_osm_data import extract_osm_data


class TestExtractOsmData(unittest.TestCase):
    def setUp(self):
        # Clean all previous export before test
        for file in os.listdir('data'):
            os.remove(os.path.join('data', file))

    def test_building_simple(self):
        # Extract building near CartONG
        extract_osm_data('building', '45.5680805, 5.9201295, 45.5682963, 5.9205333', 'CartONG')

        # Check CartONG was exported
        cartong_found = False
        tree = ET.parse(os.path.join('data', os.listdir('data')[0]))
        root = tree.getroot()
        for elem in root:
            if elem.tag == 'way':
                osm_tags = {}
                for child in elem:
                    if child.tag == 'tag':
                        osm_tags[child.attrib['k']] = child.attrib['v']
                if 'addr:city' in osm_tags and osm_tags['addr:city'] == 'Chambéry' and \
                        'addr:housenumber' in osm_tags and osm_tags['addr:housenumber'] == '23' and \
                        'addr:postcode' in osm_tags and osm_tags['addr:postcode'] == '73000' and \
                        'addr:street' in osm_tags and osm_tags['addr:street'] == 'Boulevard du Musée':
                    cartong_found = True
        self.assertTrue(cartong_found)

    def test_building_in_relation(self):
        # Extract Grenoble town hall
        extract_osm_data('building', ' 45.1867, 5.7365,  45.1867375, 5.7365261', 'Grenoble_townhall')

        # Check the Grenoble town hall was exported
        grenoble_town_hall_found = False
        way_nb = 0
        tree = ET.parse(os.path.join('data', os.listdir('data')[0]))
        root = tree.getroot()
        for elem in root:
            if elem.tag == 'way':
                way_nb += 1
            if elem.tag == 'relation':
                osm_tags = {}
                for child in elem:
                    if child.tag == 'tag':
                        osm_tags[child.attrib['k']] = child.attrib['v']
                if 'amenity' in osm_tags and osm_tags['amenity'] == 'townhall' and \
                        'name' in osm_tags and osm_tags['name'] == 'Hôtel de ville de Grenoble':
                    grenoble_town_hall_found = True
        self.assertTrue(grenoble_town_hall_found)
        self.assertEqual(2, way_nb)


if __name__ == '__main__':
    unittest.main()
