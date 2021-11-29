import context
from unittest import TestCase
from bdqc_taxa.gbif import Species
from typing import List


class TestSpecies(TestCase):
    def test_get(self, key = 9036008):
        result = Species.get(key=key)
        self.assertIsInstance(result, dict)
        self.assertTrue(all(k in result.keys() for k in [
            'key', 'scientificName'
        ]))
        self.assertTrue(all([v for k, v in result.items()
                             if k not in [
                                 'synonym', 'nomenclaturalStatus', 'remarks',
                                 'numDescendants', 'issues']]))

    def test_match_from_name(self, name='Antigone canadensis'):
        result = Species.match(name=name)
        self.assertIsInstance(result, dict)
        self.assertTrue(all(k in result.keys() for k in [
            'usageKey', 'scientificName'
        ]))
        self.assertTrue(all([v for k, v in result.items()
                             if k not in ['synonym']]))

    def test_match_from_name_kingdom(self,
                                     name='Coleoptera', kingdom='Plantae'):
        result = Species.match(name=name, kingdom = kingdom)
        self.assertIsInstance(result, dict)
        self.assertTrue(all(k in result.keys() for k in [
            'usageKey', 'scientificName'
        ]))
        self.assertTrue(all([v for k, v in result.items()
                             if k not in ['synonym']]))

    def test_get_vernacular_name(self, species_id=2474953):
        results = Species.get_vernacular_name(species_id)
        self.assertTrue(len(results) > 1)
        for result in results:
            self.assertTrue(all([v for k, v in result.items()
                                 if k not in ['preferred']]))
