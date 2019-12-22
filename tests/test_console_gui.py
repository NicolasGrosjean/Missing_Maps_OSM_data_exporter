import unittest

from src.console_gui import read_osm_full_history_config


class TestConsoleGui(unittest.TestCase):
    def test_read_osm_full_history_config(self):
        config = read_osm_full_history_config()
        self.assertEqual(config[0]['tag'], 'building')
        self.assertEqual(config[0]['tag_type'], 'polygon')
        self.assertEqual(config[1]['tag'], 'highway')
        self.assertEqual(config[1]['tag_type'], 'line')
        self.assertEqual(config[2]['tag'], 'landuse')
        self.assertEqual(config[2]['tag_type'], 'polygon')
        self.assertEqual(config[3]['tag'], 'natural')
        self.assertIsNone(config[3]['tag_type'])
        self.assertEqual(config[4]['tag'], 'water')
        self.assertIsNone(config[4]['tag_type'])


if __name__ == '__main__':
    unittest.main()
