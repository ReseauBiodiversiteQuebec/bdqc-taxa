# test_wikidata.py

import unittest

from bdqc_taxa import wikidata

# Test case : chiroptera, Q28425


class TestWikidata(unittest.TestCase):
    def test_search_entities(self, query='chiroptera'):
        searches = wikidata.search_entities(query)
        # Assert there is at least one result
        self.assertGreater(len(searches), 0)
        # Assert dict contains field 'id'
        self.assertIn('id', searches[0])

    def test_get_entities(self, id='Q28425'):
        entity = wikidata.get_entities(id)
        # Assert dict contains fields :'aliases', 'descriptions', 'labels', 'claims', 'sitelinks'
        self.assertIn('aliases', entity)
        self.assertIn('descriptions', entity)
        self.assertIn('labels', entity)
        self.assertIn('claims', entity)
        self.assertIn('sitelinks', entity)

    def test_get_entities_error(self, id='Q284ASDFAWE25'):
        with self.assertRaises(Exception):
            entity = wikidata.get_entities(id, languages=['fr'])