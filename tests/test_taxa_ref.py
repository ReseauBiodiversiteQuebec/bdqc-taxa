import unittest

import global_names
import context
from bdqc_taxa import taxa_ref

class TestFindAuthorship(unittest.TestCase):
    def test_species_author(self):
        name = 'Grus canadensis (Linnaeus, 1758)'
        name_simple = 'Grus canadensis'
        authorship = taxa_ref.find_authorship(name, name_simple)
        self.assertEqual(authorship, "Linnaeus, 1758")

    # def test_species_author_du_roi(self):
    #     name = 'Grus canadensis (Linnaeus, 1758)'
    #     name_simple = 'Grus canadensis'
    #     authorship = taxa_ref.find_authorship(name, name_simple)
    #     self.assertEqual(authorship, "Linnaeus, 1758")

    def test_subspecies_author(self):
        name = 'Spinus tristis tristis (Linnaeus, 1758)'
        name_simple = 'Spinus tristis tristis'
        authorship = taxa_ref.find_authorship(name, name_simple)
        self.assertEqual(authorship, "Linnaeus, 1758")

    def test_genus_author(self):
        name = 'Acer L.'
        name_simple = 'Acer'
        authorship = taxa_ref.find_authorship(name, name_simple)
        self.assertEqual(authorship, "L.")

    def test_family_author(self):
        name = 'Passeridae Rafinesque, 1815'
        name_simple = 'Passeridae'
        authorship = taxa_ref.find_authorship(name, name_simple)
        self.assertEqual(authorship, "Rafinesque, 1815")

class TestTaxaRef(unittest.TestCase):
    def test_from_global_names(self, name = 'Acer saccharum'):
        refs = taxa_ref.TaxaRef.from_global_names(name)
        self.assertTrue(len(refs) > 1)
        [self.assertTrue(v) for ref in refs for k, v in vars(ref).items() 
        if k not in ['id', 'match_type', 'authorship', 'rank_order', 'is_parent']
        ]
        self.assertTrue(any([ref.match_type for ref in refs]))
        self.assertTrue(any([ref.authorship for ref in refs]))
        self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
        self.assertTrue(all([ref.rank.lower() == ref.rank for ref in refs]))
        self.assertTrue(all([ref.rank != 11 for ref in refs]))

    def test_from_gbif(self, name = 'Acer saccharum'):
        refs = taxa_ref.TaxaRef.from_gbif(name)
        self.assertTrue(len(refs) > 1)
        [self.assertTrue(v) for ref in refs for k, v in vars(ref).items() 
        if k not in ['id', 'match_type', 'authorship', 'rank_order', 'is_parent']
        ]
        self.assertTrue(any([ref.match_type for ref in refs]))
        self.assertTrue(any([ref.authorship for ref in refs]))
        self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
        self.assertTrue(all([ref.rank.lower() == ref.rank for ref in refs]))

    def test_from_gbif_w_authorship(self, name = 'Acer saccharum',
            authorship = 'Pax'):
        refs = taxa_ref.TaxaRef.from_gbif(name, authorship)
        self.assertTrue(len(refs) > 1)
        [self.assertTrue(v) for ref in refs for k, v in vars(ref).items() 
        if k not in ['id', 'match_type', 'authorship', 'rank_order', 'is_parent']
        ]
        self.assertTrue(any([ref.match_type for ref in refs]))
        self.assertTrue(any([ref.authorship for ref in refs]))
        self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
        self.assertTrue(all([ref.rank.lower() == ref.rank for ref in refs]))

    def test_from_all_sources(self, name = 'Acer saccharum'):
        refs = taxa_ref.TaxaRef.from_all_sources(name)
        self.assertTrue(len(refs) > 1)
        ref_sources_id = {ref.source_id for ref in refs}
        pref_sources = global_names.PREFFERED_SOURCES + [11]
        self.assertTrue(all([v in ref_sources_id for v in pref_sources]))

    # def test_from_global_names(self, name = 'formica querquetulana', authorship = 'Kennedy & Davis, 1937'):
    #     refs = taxa_ref.TaxaRef.from_global_names(name, authorship)
    #     [self.assertTrue(v) for ref in refs for k, v in vars(ref).items() 
    #     if k not in ['id', 'match_type', 'authorship', 'rank_order']
    #     ]
    #     self.assertTrue(any([ref.match_type for ref in refs]))
    #     self.assertTrue(any([ref.authorship for ref in refs]))
    #     self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))