import sys
import time
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digHeightWeightExtractor.height_weight_extractor import HeightWeightExtractor

class TestHeightWeightExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_height_weight_extractor(self):
        doc = {'content': "\n TS RUBI: THE NAME SAYS IT ALL!  \n INCALL $250 OUTCALL $350 \n \n \n \n \n \n Gender \n Age \n Ethnicity \n Hair Color \n Eye Color \n Height \n Weight \n Measurements \n Affiliation \n Availability \n Available To \n \n \n \n \n Transsexual \n 27 \n Latino/Hispanic \n Brown \n Hazel \n 5'5\" \n 130 lb \n 34C - 28\" - 34\" \n ", 'b': 'world'}

        extractor = HeightWeightExtractor().set_metadata({'extractor': 'height_weight'})
        extractor_processor = ExtractorProcessor().set_input_fields(['content']).set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['extracted'][0]['value'], {'height': [{'foot': 5, 'inch': 5}], 'weight': [{'pound': 130}]})
    

if __name__ == '__main__':
    unittest.main()



