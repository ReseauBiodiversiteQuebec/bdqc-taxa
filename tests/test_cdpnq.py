# Test for the cdpnq match function using unittest

import unittest

from bdqc_taxa import cdpnq

class TestCdpnq(unittest.TestCase):
    def test_match_species(self, name = 'Libellula luctuosa'):
        result = cdpnq.match_taxa(name)
        self.assertEqual(result['name'], name)
        self.assertEqual(result['rank'], 'species')
        
    def test_no_match(self, name = 'Vincent Beauregard'):
        result = cdpnq.match_taxa(name)
        self.assertEqual(result, None)

    def test_match_synonym(self, name = 'Gomphus borealis'):
        result = cdpnq.match_taxa(name)
        self.assertEqual(result['valid_name'], 'Phanogomphus borealis')
        self.assertEqual(result['rank'], 'species')

    def test_match_genus(self, name = 'Libellula'):
        result = cdpnq.match_taxa(name)
        self.assertEqual(result['name'], 'Libellula')
        self.assertEqual(result['rank'], 'genus')

    def test_match_canonical(self, name = 'Libellula luctuosa Burmeister, 1839'):
        result = cdpnq.match_taxa(name)
        self.assertEqual(result['name'], 'Libellula luctuosa')
        self.assertEqual(result['rank'], 'species')