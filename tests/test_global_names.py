from bdqc_taxa import global_names
from unittest import TestCase
import context

class TestGlobalNames(TestCase):
    def test_verify(self, name = 'Acer saccharum'):
        result: list = global_names.verify(name)
        self.assertIsInstance(result, list)
        [self.assertTrue(bool(v)) for k, v in result[0].items()]

    def test_verify_no_result(self, name = 'Vincent Beauregard'):
        result: list = global_names.verify(name)
        self.assertIsInstance(result, list)
        self.assertTrue(result[0]['matchType'] == 'NoMatch')
