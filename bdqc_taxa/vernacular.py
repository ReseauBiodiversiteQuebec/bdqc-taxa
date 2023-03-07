from . import gbif
from . import bryoquel
from . import cdpnq
from . import taxa_ref
from inspect import signature
from typing import Union, List

# ACCEPTED_DATA_SOURCE = [
#     'Integrated Taxonomic Information System (ITIS)',
#     'Catalogue of Life Checklist']

ACCEPTED_LANGUAGE = ['fra', 'eng']

def initcap(sentence):
    sentence = sentence.lower()
    return " ".join(
        [word[0].upper() + word[1:].lower() for word in sentence.split(" ")]
    )

class Vernacular:
    def __init__(self,
                 name: str = '',
                 source: str = '',
                 source_taxon_key: str = '',
                 language: str = ''):
        for param in signature(self.__init__).parameters:
            setattr(self, param, eval(param))
        self.language = language.lower()
        self.name = name.lower()
    
    @classmethod
    def from_gbif(cls, gbif_key: int):
        out = []
        gbif_results = gbif.Species.get_vernacular_name(gbif_key)
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
        species = gbif.Species.match(name = name, **match_kwargs)
        try:
            return cls.from_gbif(species['usageKey'])
        except KeyError:
            return []

    @classmethod
    def from_bryoquel_match(cls, name: str = ''):
        species = bryoquel.match_taxa(name)
        if species:
            return [cls(
                name = species['vernacular_name_fr'],
                source = 'Bryoquel',
                language = 'fra',
                source_taxon_key = species['id']
            ), cls(
                name = species['vernacular_name_en'],
                source = 'Bryoquel',
                language = 'eng',
                source_taxon_key = species['id']
            )]
        else:
            return []

    @classmethod
    def from_cdpnq_match(cls, name: str = ''):
        taxas = cdpnq.match_taxa(name)
        if not taxas:
            return []
        out = []
        for taxa in taxas:
            out.append(cls(
                name = taxa['vernacular_fr'],
                source = 'CDPNQ',
                language = 'fra',
                source_taxon_key = taxa['name']
            ))
        
        return out


    @classmethod
    def from_match(cls, name: str = None, **match_kwargs):
        name = [name] if name else []
        match = taxa_ref.TaxaRef.from_all_sources(name[0])
        name = {m.scientific_name for m in match if not m.is_parent}

        gbif_keys = {m.source_record_id for m in match
            if m.source_name == 'GBIF Backbone Taxonomy' and not m.is_parent}
        out = []
        [out.extend(cls.from_gbif(gbif_key=k, **match_kwargs)) for k in gbif_keys]
        [out.extend(cls.from_bryoquel_match(n, **match_kwargs)) for n in name]
        [out.extend(cls.from_cdpnq_match(n, **match_kwargs)) for n in name]
        
        return out