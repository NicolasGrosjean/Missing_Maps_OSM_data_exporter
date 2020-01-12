import datetime
import unittest

from src.console_gui import read_osm_full_history_config, check_date_format


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
        self.assertEqual(config[4]['tag'], 'waterway')
        self.assertIsNone(config[4]['tag_type'])

    def test_date_format(self):
        self.assertFalse(check_date_format(''))
        self.assertFalse(check_date_format('2019'))
        self.assertFalse(check_date_format('2019-11'))
        self.assertTrue(check_date_format('2019-11-12'))
        self.assertFalse(check_date_format('2019/11/12'))
        self.assertTrue(check_date_format('2019-11-24'))
        self.assertFalse(check_date_format('2019-24-12'))
        self.assertFalse(check_date_format('a-b-c'))
        self.assertFalse(check_date_format('1019-2-12'))
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        self.assertFalse(check_date_format(tomorrow.strftime('%Y-%m-%d')))
        self.assertTrue(check_date_format('2019-2-12'))
        self.assertFalse(check_date_format('2019-11-12T'))


if __name__ == '__main__':
    unittest.main()
