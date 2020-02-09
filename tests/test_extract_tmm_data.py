import os
import shutil
import unittest

import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.extract_tmm_data import TmmProjectDatabase, extend_bounding_box


def get_bbox():
    project_id = 5654
    db = TmmProjectDatabase(project_id)
    os.makedirs(os.path.join('data', str(project_id)), exist_ok=True)
    bbox = db.get_perimeter_bbox()
    return bbox


class TestExtractTmmData(unittest.TestCase):
    def setUp(self):
        os.makedirs('data', exist_ok=True)
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

    def test_extend_bounding_box(self):
        bbox = [0, 0, 1, 1]
        new_bbox = extend_bounding_box(bbox, 20)
        self.assertAlmostEqual(1.2, (new_bbox[2] - new_bbox[0]) * (new_bbox[3] - new_bbox[1]), delta=0.01)


if __name__ == '__main__':
    unittest.main()
