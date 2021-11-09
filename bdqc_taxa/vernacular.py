from gbif import Species
from inspect import signature

# ACCEPTED_DATA_SOURCE = [
#     'Integrated Taxonomic Information System (ITIS)',
#     'Catalogue of Life Checklist']

ACCEPTED_LANGUAGE = ['fra', 'eng']

class Vernacular:
    def __init__(self,
                 name: str = '',
                 source: str = '',
                 source_taxon_key: str = '',
                 language: str = ''):
        for param in signature(self.__init__).parameters:
            setattr(self, param, eval(param))
    
    @classmethod
    def from_gbif(cls, gbif_key: int):
        out = []
        gbif_results = Species.get_vernacular_name(gbif_key)
        for result in gbif_results:
            if result['language'] not in ACCEPTED_LANGUAGE:
                continue
            out.append(
                cls(
                    name = result['vernacularName'],
                    source = result['source'],
                    language = result['language'],
                    source_taxon_key = result['sourceTaxonKey']
                )
            )
        # dict comprehension trick to get only unique objects
        out = list({str(vars(o)): o for o in out}.values())
        return out
    
    @classmethod
    def from_gbif_match(cls, name: str = '', **match_kwargs):
        species = Species.match(name = name, **match_kwargs)
        return cls.from_gbif(species['usageKey'])
