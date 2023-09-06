from . import gbif
from . import bryoquel
from . import cdpnq
from . import taxa_ref
from . import wikidata

# ACCEPTED_DATA_SOURCE = [
#     'Integrated Taxonomic Information System (ITIS)',
#     'Catalogue of Life Checklist']

ACCEPTED_LANGUAGE = ['fra', 'eng']

def initcap_vernacular(name):
    capped_words = ['Amérique', 'America', 'Europe', 'Ungava', 'Alléghanys', 'Oregon', 'Virginie', 'Virginia', 'New York', 'Alaska', 'Pennsylvanie', 'Pennsylvania' , 'Canada', 'Inde', 'India', 'Islande', 'Égypte', 'Egypt', 'Pacifique', 'Pacific', 'Atlantique', 'Atlantic', 'Fraser', 'Est', 'Ouest', 'Nord', 'Alep', 'Anadyr', 'Eames', 'Allen', 'Anna', 'Uhler', 'Audubon']
    capped_words_lower = [word.lower() for word in capped_words]
    out = name[0].upper() + name[1:].lower()
    out_list = out.split(' ')
    for i, word in enumerate(out_list):
        if word.lower() in capped_words_lower:
            out_list[i] = out_list[i].capitalize()
    out = ' '.join(out_list)
    return out


class Vernacular:
    def __init__(self,
                 name: str = '',
                 source: str = '',
                 source_taxon_key: str = '',
                 language: str = ''):
        self._name = name
        self.source = source
        self.source_taxon_key = source_taxon_key
        self.language = language.lower()

    @property
    def name(self):
        return initcap_vernacular(self._name)

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
        out = []
        if species and species['vernacular_name_fr']:
            out = [*out, cls(
                    name = species['vernacular_name_fr'],
                    source = 'Bryoquel',
                    language = 'fra',
                    source_taxon_key = species['id']
                )]
        if species and species['vernacular_name_en']:
            out = [*out, cls(
                    name = species['vernacular_name_en'],
                    source = 'Bryoquel',
                    language = 'eng',
                    source_taxon_key = species['id']
                )]
        return out

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
    def from_wikidata_match(cls, name: str = ''):
        result = wikidata.search_entities(name)[0]
        entity = wikidata.get_entities(result['id'], languages=['fr', 'en'])
        out = []

        language_dict = {
            'fr': 'fra',
            'en': 'eng'
        }

        # For each language, we only keep the first result that is not a scientific name
        for language in language_dict.keys():
            try:
                name_dicts = [entity['labels'][language]]
            except KeyError:
                name_dicts = []

            try:
                name_dicts += entity['aliases'][language]
            except KeyError:
                pass

            if not name_dicts:
                continue

            for name_dict in name_dicts:
                vernacular = cls(
                    name = name_dict['value'],
                    source = 'Wikidata',
                    language = language_dict[language],
                    source_taxon_key = result['id']
                )
                if vernacular.name.lower() != name.lower():
                    out.append(vernacular)
                    break
        
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
        # [out.extend(cls.from_bryoquel_match(n, **match_kwargs)) for n in name]
        [out.extend(cls.from_cdpnq_match(n, **match_kwargs)) for n in name]
        [out.extend(cls.from_wikidata_match(n, **match_kwargs)) for n in name]
        
        return out