from unittest import TestCase, result
from bdqc_taxa.vernacular import Vernacular, initcap_vernacular

class TestVernacular(TestCase):
    def assertVernacularList(self, results):
        self.assertTrue(results.__len__() >= 1)
        self.assertTrue(all([vn.language in ['fra', 'eng'] for vn in results]))

    def test_from_gbif(self, gbif_key = 2474953):
        results = Vernacular.from_gbif(gbif_key)
        self.assertVernacularList(results)
    
    def test_from_gbif_non_unique(self, gbif_key = 2474953):
        results = Vernacular.from_gbif(gbif_key)
        unique_results = {str(vars(o)): o for o in results}.values()
        self.assertEqual(len(results), len(unique_results))


    def test_from_gbif_invalid_key(self, gbif_key = 9036008):
        results = Vernacular.from_gbif(gbif_key)
        self.assertVernacularList(results)

    def test_from_gbif_match(self, name = 'Cyanocitta cristata'):
        results = Vernacular.from_gbif_match(name)
        self.assertVernacularList(results)

    
    def test_from_gbif_match_no_match(self, name = 'Vincent Beauregard'):
        results = Vernacular.from_gbif_match(name)
        self.assertIsInstance(results, list)
        
        # Assert empty list
        self.assertEqual(len(results), 0)

    def test_from_gbif_match_passing_kwargs(self,
        name = 'Cyanocitta cristata',
        kingdom = 'Animalia'):
        results = Vernacular.from_gbif_match(name, kingdom = kingdom)
        self.assertVernacularList(results)

    def test_from_match(self, name = 'Cyanocitta cristata'):
        results = Vernacular.from_match(name)
        self.assertVernacularList(results)
    
    def test_from_match_no_match(self, name = 'Vincent Beauregard'):
        results = Vernacular.from_match(name)
        self.assertIsInstance(results, list)
        
        # Assert empty list
        self.assertEqual(len(results), 0)

    def test_from_bryoquel_match(self, name = 'Aulacomnium palustre'):
        results = Vernacular.from_bryoquel_match(name)
        self.assertVernacularList(results)

    def test_from_bryoquel_no_vernacular(self, name = 'Aulacomnium'):
        results = Vernacular.from_bryoquel_match(name)
        self.assertFalse(results)

    def test_from_bryoquel_no_match(self, name = 'Vincent Beauregard'):
        results = Vernacular.from_bryoquel_match(name)
        self.assertIsInstance(results, list)
        
        # Assert empty list
        self.assertEqual(len(results), 0)
    
    def test_from_cdpnq_match(self, name = 'Libellula luctuosa'):
        results = Vernacular.from_cdpnq_match(name)
        self.assertVernacularList(results)
        self.assertTrue(any([vn.source == 'CDPNQ' for vn in results]))

    def test_get_cdpnq(self, name = 'Libellula luctuosa'):
        results = Vernacular.from_cdpnq_match(name)
        self.assertVernacularList(results)
        self.assertTrue(any([vn.source == 'CDPNQ' for vn in results]))
    
    def test_get_cdpnq_no_match(self, name = 'Vincent Beauregard'):
        results = Vernacular.from_cdpnq_match(name)
        self.assertFalse(results)

    # Special case test: Synonym scientific name is not in CDPNQ : Bug #5
    def test_synonym_cdpnq(self, name = 'Libellula julia'):
        results = Vernacular.from_match(name)
        self.assertVernacularList(results)
        self.assertTrue(any([vn.source == 'CDPNQ' for vn in results]))

    def test_moineau(self, name = 'Passer domesticus'):
        results = Vernacular.from_match(name)
        self.assertVernacularList(results)
        self.assertTrue(any([vn.source == 'CDPNQ' for vn in results]))
        # Asser that the vernacular is 'Moineau domestique'
        self.assertTrue(any([vn.name == 'Moineau domestique' for vn in results]))

class TestInitcap(TestCase):
    def test_initcap_vernacular(self, text = 'Vincent Beauregard'):
        self.assertEqual(initcap_vernacular(text), 'Vincent beauregard')
    
    def test_initcap_no_change(self, text = 'Lynx du Canada'):
        self.assertEqual(initcap_vernacular(text), text)

    def test_initcap_all_caps(self, text = 'LYNX DU CANADA'):
        self.assertEqual(initcap_vernacular(text), 'Lynx du Canada')
    
    def test_initcap_all_lower(self, text = 'millepertuis de fraser'):
        self.assertEqual(initcap_vernacular(text), 'Millepertuis de Fraser')

    def test_initcap_nordique(self, text = 'Chauve-souris nordique'):
        self.assertEqual(initcap_vernacular(text), text)

    def test_initcap_moineau(self, text = 'Moineau domestique'):
        self.assertEqual(initcap_vernacular(text), text)