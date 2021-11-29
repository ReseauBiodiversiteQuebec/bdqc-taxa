from unittest import TestCase, result
from bdqc_taxa.vernacular import Vernacular

class TestVernacular(TestCase):
    def assertVernacularList(self, results):
        self.assertTrue(results.__len__() > 1)
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

    def test_from_gbid_match_passing_kwargs(self,
        name = 'Cyanocitta cristata',
        kingdom = 'Animalia'):
        results = Vernacular.from_gbif_match(name, kingdom = kingdom)
        self.assertVernacularList(results)