# Test the bryoquel module

from unittest import TestCase
from bdqc_taxa.bryoquel import match_taxa

class TestBryoquel(TestCase):
    def test_match_species(self, species='Aulacomnium palustre'):
        # Test a species that is in the database
        result = match_taxa(species)
        self.assertEqual(result['id'], "ID269")
        self.assertEqual(result['family'], 'Aulacomniaceae')
        self.assertEqual(result['scientific_name'], 'Aulacomnium palustre')
        self.assertEqual(result['canonical_full'], 'Aulacomnium palustre (Hedw.) Schwägr.')
        self.assertEqual(result['vernacular_name_fr'], 'aulacomnie des marais')
        self.assertEqual(result['vernacular_name_en'], 'ribbed bog moss')
        self.assertEqual(result['clade'], 'Musci')
        self.assertEqual(result['authorship'], '(Hedw.) Schwägr.')

    def test_match_species_canonical(self, species='Aulacomnium palustre (Hedw.) Schwägr.'):
        # Test a species that is in the database
        result = match_taxa(species)
        self.assertEqual(result['id'], "ID269")
        self.assertEqual(result['family'], 'Aulacomniaceae')
        self.assertEqual(result['scientific_name'], 'Aulacomnium palustre')
        self.assertEqual(result['vernacular_name_fr'], 'aulacomnie des marais')
        self.assertEqual(result['vernacular_name_en'], 'ribbed bog moss')
        self.assertEqual(result['clade'], 'Musci')
        self.assertEqual(result['authorship'], '(Hedw.) Schwägr.')

    def test_match_family(self, family='Aulacomniaceae'):
        # Test a species that is in the database
        result = match_taxa(family)
        self.assertEqual(result['family'], 'Aulacomniaceae')
        self.assertEqual(result['scientific_name'], 'Aulacomniaceae')
        self.assertEqual(result['vernacular_name_fr'], None)
        self.assertEqual(result['vernacular_name_en'], None)
        self.assertEqual(result['clade'], 'Musci')
        self.assertEqual(result['authorship'], None)
