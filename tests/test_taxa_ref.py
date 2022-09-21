import unittest

import context
from bdqc_taxa import taxa_ref
from bdqc_taxa import global_names


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
    def test_dict_dunder(self):
        name = 'Lasiurus cinereus'
        tr = taxa_ref.TaxaRef(name)
        self.assertTrue(isinstance(tr.__dict__, dict))

    def test_repr(self):
        name = 'Lasiurus cinereus'
        tr = taxa_ref.TaxaRef(name)
        self.assertEqual(repr(tr), f"TaxaRef('{name}')")
    
    def test_str(self):
        name = 'Lasiurus cinereus'
        tr = taxa_ref.TaxaRef(name)
        self.assertEqual(str(tr), name)

    def test_from_global_names(self, name='Acer saccharum'):
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

        # Bug: Bad authorship value, equals scientific_name
        bad_refs = [
            ref for ref in refs
            if ref.authorship
                and ref.authorship == ref.scientific_name
        ]
        self.assertFalse(bad_refs)


    def test_from_global_names_no_match(self, name='Vincent Beauregard'):
        refs = taxa_ref.TaxaRef.from_global_names(name)
        self.assertFalse(refs)

    def test_from_gbif(self, name='Acer saccharum'):
        refs = taxa_ref.TaxaRef.from_gbif(name)
        self.assertTrue(len(refs) > 1)
        [self.assertTrue(v) for ref in refs for k, v in vars(ref).items()
         if k not in ['id', 'match_type', 'authorship', 'rank_order', 'is_parent']
         ]
        self.assertTrue(any([ref.match_type for ref in refs]))
        self.assertTrue(any([ref.authorship for ref in refs]))
        self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
        self.assertTrue(all([ref.rank.lower() == ref.rank for ref in refs]))
        self.assertTrue(len({(ref.valid, ref.rank_order) for ref in refs}) ==
                        len(refs))

        # Bug: Bad authorship value, equals scientific_name
        bad_refs = [
            ref for ref in refs
            if ref.authorship
                and ref.authorship == ref.scientific_name
        ]
        self.assertFalse(bad_refs)


    def test_from_gbif(self, name='Antigone canadensis'):
        refs = taxa_ref.TaxaRef.from_gbif(name)
        self.assertTrue(len(refs) > 1)
        [self.assertTrue(v) for ref in refs for k, v in vars(ref).items()
         if k not in ['id', 'match_type', 'authorship', 'rank_order',
                      'is_parent', 'valid']
         ]
        self.assertTrue(any([ref.match_type for ref in refs]))
        self.assertTrue(any([ref.authorship for ref in refs]))
        self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
        self.assertTrue(all([ref.rank.lower() == ref.rank for ref in refs]))
        self.assertTrue(len({(ref.valid, ref.rank_order) for ref in refs}) ==
                        len(refs))

        # Bug: Bad authorship value, equals scientific_name
        bad_refs = [
            ref for ref in refs
            if ref.authorship
                and ref.authorship == ref.scientific_name
        ]
        self.assertFalse(bad_refs)


    def test_from_gbif_bug_acceptedKey_error(
            self, name='Kobresia simpliciuscula subholarctica (T.V.Egorova) Saarela'):
        refs = taxa_ref.TaxaRef.from_gbif(name)
        self.assertTrue(len(refs) > 1)
        [self.assertTrue(v) for ref in refs for k, v in vars(ref).items()
         if k not in ['id', 'match_type', 'authorship', 'rank_order',
                      'is_parent', 'valid']
         ]
        self.assertTrue(any([ref.match_type for ref in refs]))
        self.assertTrue(any([ref.authorship for ref in refs]))
        self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
        self.assertTrue(all([ref.rank.lower() == ref.rank for ref in refs]))
        self.assertTrue(len({(ref.valid, ref.rank_order) for ref in refs}) ==
                        len(refs))

    def test_from_gbif_bug_rank_key_error(
            self, name='Ranunculus arcticus (R. Br.) L. D. Benson'):
        refs = taxa_ref.TaxaRef.from_gbif(name)
        self.assertTrue(len(refs) > 1)
        [self.assertTrue(v) for ref in refs for k, v in vars(ref).items()
         if k not in ['id', 'match_type', 'authorship', 'rank_order',
                      'is_parent', 'valid']
         ]
        self.assertTrue(any([ref.match_type for ref in refs]))
        self.assertTrue(any([ref.authorship for ref in refs]))
        self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
        self.assertTrue(all([ref.rank.lower() == ref.rank for ref in refs]))
        self.assertTrue(len({(ref.valid, ref.rank_order) for ref in refs}) ==
                        len(refs))

    def test_from_gbif_w_authorship(self, name='Acer saccharum',
                                    authorship='Pax'):
        refs = taxa_ref.TaxaRef.from_gbif(name, authorship)
        self.assertTrue(len(refs) > 1)
        [self.assertTrue(v) for ref in refs for k, v in vars(ref).items()
         if k not in ['id', 'match_type', 'authorship', 'rank_order',
                      'is_parent', 'valid']
         ]
        self.assertTrue(any([ref.match_type for ref in refs]))
        self.assertTrue(any([ref.authorship for ref in refs]))
        self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
        self.assertTrue(all([ref.rank.lower() == ref.rank for ref in refs]))

    def test_from_gbif_no_match(self, name='Vincent Beauregard'):
        refs = taxa_ref.TaxaRef.from_gbif(name)
        self.assertFalse(refs)

    def test_from_gbif_invalid_subspecies(self, name='Circus hudsonius'):
        refs = taxa_ref.TaxaRef.from_gbif(name)
        self.assertTrue(len(refs) > 1)
        self.assertTrue(any([ref.rank == 'subspecies' for ref in refs]))

    def test_from_all_sources(self, name='Acer saccharum'):
        refs = taxa_ref.TaxaRef.from_all_sources(name)
        self.assertTrue(len(refs) > 1)
        ref_sources_id = {ref.source_id for ref in refs}
        pref_sources = global_names.DATA_SOURCES + [11]
        self.assertTrue(all([v in ref_sources_id for v in pref_sources]))

class TestComplex(unittest.TestCase):
    def test_complex_is_true(self,
                             name='Lasiurus cinereus|Lasionycteris noctivagans'):
        out = taxa_ref.is_complex(name)
        self.assertTrue(out)

    def test_complex_is_false(self, name='Lasionycteris noctivagans'):
        out = taxa_ref.is_complex(name)
        self.assertFalse(out)

    def test_from_all_sources(self,
                              name='Lasiurus cinereus|Lasionycteris noctivagans'):

        refs = taxa_ref.TaxaRef.from_all_sources(name)
        self.assertTrue(len(refs) > 1)

        is_match_complex = [ref.match_type == "complex" for ref in refs]
        self.assertTrue(
            any(is_match_complex) and not all(is_match_complex)
        )
        is_common_parent = [ref.match_type ==
                            "complex_closest_parent" for ref in refs]
        self.assertTrue(
            sum(is_common_parent) == len({ref.source_id for ref in refs})
        )

        distinct_srid = {(r.source_id, r.source_record_id) for r in refs}
        self.assertTrue(
            len(refs) == len(distinct_srid)
        )

        # BUG: For a single source, all but one match_type is complex
        source_null_match = {ref.source_name: [] for ref in refs}
        [source_null_match[ref.source_name].append(not bool(ref.match_type))
            for ref in refs]
        self.assertTrue(all([any(nulls)
                        for nulls in source_null_match.values()]))

        # BUG: Complex_closest_parent for wrong ref
        source_names = list({ref.source_name for ref in refs})
        source_max_rank = {
            src: max(
                [ref.rank_order for ref in refs if src == ref.source_name])
            for src in source_names}
        source_match_rank = {src: ref.rank_order
                             for src in source_names
                             for ref in refs
                             if ref.match_type == "complex_closest_parent"}
        self.assertFalse(
            any(
                [source_max_rank[src] == source_match_rank[src]
                    for src in source_names]))

        # BUG: Only one valid ref from GBIF
        gbif_refs = [
            ref for ref in refs
            if ref.source_name == 'GBIF Backbone Taxonomy'
                and ref.valid
                and ref.match_type == "complex"
                and ref.rank == "species"
        ]
        self.assertTrue(len(gbif_refs) == 2)

    # def test_from_global_names(self, name = 'formica querquetulana', authorship = 'Kennedy & Davis, 1937'):
    #     refs = taxa_ref.TaxaRef.from_global_names(name, authorship)
    #     [self.assertTrue(v) for ref in refs for k, v in vars(ref).items()
    #     if k not in ['id', 'match_type', 'authorship', 'rank_order']
    #     ]
    #     self.assertTrue(any([ref.match_type for ref in refs]))
    #     self.assertTrue(any([ref.authorship for ref in refs]))
    #     self.assertTrue(all([isinstance(ref.rank_order, int) for ref in refs]))
