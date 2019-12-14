import os
import shutil
import unittest

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.extract_tmm_data import TmmProjectDatabase


def get_bbox():
    project_id = 5654
    db = TmmProjectDatabase(project_id)
    os.makedirs(os.path.join('data', str(project_id)), exist_ok=True)
    #db.export_perimeter(os.path.join('data', str(project_id), 'perimeter.json'))
    bbox = db.get_perimeter_bbox()
    return bbox


class TestExtractTmmData(unittest.TestCase):
    def setUp(self):
        # Clean all previous export before test
        shutil.rmtree('data')

    def test_building_simple(self):
        # Test with downloading data
        bbox = get_bbox()
        self.assertAlmostEqual(-1.66373937010386, bbox[0])
        self.assertAlmostEqual(12.2784694870073, bbox[1])
        self.assertAlmostEqual(-1.58506481527903, bbox[2])
        self.assertAlmostEqual(12.3407795046204, bbox[3])

        # Test without downloading data
        bbox = get_bbox()
        self.assertAlmostEqual(-1.66373937010386, bbox[0])
        self.assertAlmostEqual(12.2784694870073, bbox[1])
        self.assertAlmostEqual(-1.58506481527903, bbox[2])
        self.assertAlmostEqual(12.3407795046204, bbox[3])


if __name__ == '__main__':
    unittest.main()
