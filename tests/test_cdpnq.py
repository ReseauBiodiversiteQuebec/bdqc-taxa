# Test for the cdpnq match function using unittest

import unittest

from bdqc_taxa import cdpnq

class TestCdpnqOdonates(unittest.TestCase):
    def test_match_species(self, name = 'Libellula luctuosa'):
        result = cdpnq.match_taxa_odonates(name)
        self.assertEqual(result['name'], name)
        self.assertEqual(result['rank'], 'species')
        
    def test_no_match(self, name = 'Vincent Beauregard'):
        result = cdpnq.match_taxa_odonates(name)
        self.assertEqual(result, None)

    def test_match_synonym(self, name = 'Gomphus borealis'):
        result = cdpnq.match_taxa_odonates(name)
        self.assertEqual(result['valid_name'], 'Phanogomphus borealis')
        self.assertEqual(result['rank'], 'species')

    def test_match_genus(self, name = 'Libellula'):
        result = cdpnq.match_taxa_odonates(name)
        self.assertEqual(result['name'], 'Libellula')
        self.assertEqual(result['rank'], 'genus')

    def test_ladona_julia(self, name = 'Ladona julia'):
        result = cdpnq.match_taxa_odonates(name)
        self.assertTrue(result['name'] == 'Ladona julia')
        self.assertTrue(result['valid_name'] == 'Ladona julia')
        self.assertTrue(result['rank'] == 'species')
        
class TestCdpnqVertebrates(unittest.TestCase):
    def test_match_species(self, name = 'Pica hudsonia'):
        result = cdpnq.match_taxa_vertebrates(name)
        self.assertEqual(result['name'], name)
        self.assertEqual(result['rank'], 'species')

    def test_no_match(self, name = 'Vincent Beauregard'):
        result = cdpnq.match_taxa_vertebrates(name)
        self.assertEqual(result, None)

    def test_match_synonym(self, name = 'Pica pica'):
        result = cdpnq.match_taxa_vertebrates(name)
        self.assertEqual(result['valid_name'], 'Pica hudsonia')
        self.assertEqual(result['rank'], 'species')

    def test_match_genus(self, name = 'Pica'):
        result = cdpnq.match_taxa_vertebrates(name)
        self.assertEqual(result['name'], 'Pica')
        self.assertEqual(result['rank'], 'genus')

    def test_no_match_taxon(self, name = 'Rana'):
        result = cdpnq.match_taxa_vertebrates(name)
        self.assertEqual(result, None)
    
    def test_rangifer_tarandus(self, name = 'Rangifer tarandus'):
        result = cdpnq.match_taxa_vertebrates(name)
        self.assertTrue(result['valid_name'] == 'Rangifer tarandus caribou')
        self.assertTrue(result['rank'] == 'species')
        self.assertTrue(result['synonym'] == 1)
        self.assertTrue(result['vernacular_fr'] == 'Caribou des bois')
        self.assertTrue(result['vernacular_en'] == 'Woodland Caribou')

# Test match_taxa for both odonates and vertebrates
class TestCdpnq(unittest.TestCase):
    def test_match_species(self, name = 'Libellula luctuosa'):
        result = cdpnq.match_taxa(name)
        self.assertEqual(result[0]['name'], name)
        self.assertEqual(result[0]['rank'], 'species')

    def test_no_match(self, name = 'Vincent Beauregard'):
        result = cdpnq.match_taxa(name)
        self.assertFalse(result)

    def test_match_vertebrates_species(self, name = 'Pica hudsonia'):
        result = cdpnq.match_taxa(name)
        self.assertEqual(result[0]['name'], name)
        self.assertEqual(result[0]['rank'], 'species')
