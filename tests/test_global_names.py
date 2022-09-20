from bdqc_taxa import global_names
from unittest import TestCase
import context

class TestGlobalNames(TestCase):
    def test_verify(self, name = 'Acer saccharum'):
        result: list = global_names.verify(name)
        # Assert that the result is a dict with keys 'metadata' and 'names'
        self.assertIsInstance(result, dict)
        self.assertTrue('metadata' in result.keys())
        self.assertTrue('names' in result.keys())

        self.assertTrue(result['names'][0]['matchType'] == 'Exact')
        self.assertIsInstance(result['names'], list)
        [self.assertTrue(bool(v)) for k, v in result['names'][0].items()]

        # Assert that the resulted names contains at least 3 names
        self.assertTrue(len(result['names'][0]['results']) >= 3)

    def test_verify_no_result(self, name = 'Vincent Beauregard'):
        result: list = global_names.verify(name)
        self.assertIsInstance(result['names'], list)
        self.assertTrue(result['names'][0]['matchType'] == 'NoMatch')
