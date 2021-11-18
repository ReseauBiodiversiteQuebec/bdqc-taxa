from os import readlink
from . import global_names
from . import gbif
from typing import List
from inspect import signature

GBIF_SOURCE_KEY = 11 # Corresponds to global names
GBIF_SOURCE_NAME = 'GBIF Backbone Taxonomy'
GBIF_RANKS = ['kingdom', 'phylum', 'class', 'order', 'family',
                'genus', 'species', 'subspecies']


class TaxaRef:
    def __init__(self,
                 id: int = None,
                 source_id: int = None,
                 source_record_id: str = '',
                 source_name: str = '',
                 scientific_name: str = '',
                 authorship: str = '',
                 rank: str = '',
                 rank_order: int = None,
                 classification_srids: List[str] = None,
                 valid: bool = None,
                 valid_srid: str = '',
                 match_type: str = '',
                 is_parent: bool = None):
        for param in signature(self.__init__).parameters:
            setattr(self, param, eval(param))
            self.rank = rank.lower()

    @classmethod
    def from_global_names(cls, name: str, authorship: str = None):
        if isinstance(authorship, str) and authorship.strip():
            name =" ".join([name, authorship])

        gn_results = global_names.verify(name)
        try:
            gn_results = [
                result for species in gn_results 
                for result in species['preferredResults']]
        except KeyError:
            return []
        out = []
        for result in gn_results:
            is_valid = result["currentRecordId"] == result["recordId"]
            if not is_valid:
                out_kwargs = {
                    "source_id": result["dataSourceId"],
                    "source_record_id": result["recordId"],
                    "source_name": result["dataSourceTitleShort"],
                    "scientific_name": result["matchedCanonicalFull"],
                    "authorship": find_authorship(
                        result["matchedName"],
                        result["matchedCanonicalFull"]),
                    "rank": result["classificationRanks"].split("|")[-1],
                    "rank_order": result["classificationRanks"].count("|") + 1,
                    "classification_srids":
                        result["classificationIds"].split("|"),
                    "valid": is_valid,
                    "valid_srid": result["currentRecordId"],
                    "match_type": result["matchType"].lower(),
                    "is_parent": False
                }
                out.append(cls(**out_kwargs))
            for rank_order, taxa_attributes in enumerate(zip(
                result["classificationPath"].split("|"),
                result["classificationRanks"].split("|"),
                result["classificationIds"].split("|"))
            ):
                taxa, rank, srid = taxa_attributes
                match_type = None
                if rank == result["classificationRanks"].split("|")[-1]:
                    valid_authorship = find_authorship(
                        result["matchedName"],
                        result["matchedCanonicalFull"])
                    is_parent = False
                    if is_valid:
                        match_type = result["matchType"].lower()
                else:
                    valid_authorship = None
                    is_parent = True
                out_kwargs = {
                        "source_id": result["dataSourceId"],
                        "source_record_id": srid,
                        "source_name": result["dataSourceTitleShort"],
                        "scientific_name": taxa,
                        "authorship": valid_authorship,
                        "rank": rank,
                        "rank_order": rank_order,
                        "classification_srids":
                            result["classificationIds"].split(
                                "|")[:rank_order + 1],
                        "valid": True,
                        "valid_srid": srid,
                        "match_type": match_type,
                        "is_parent": is_parent
                    }
                out.append(cls(**out_kwargs))
        return out

    @classmethod
    def from_gbif(cls, name: str, authorship: str = None):
        if isinstance(authorship, str) and authorship.strip():
            name =" ".join([name, authorship])
        match_species = gbif.Species.match(name)
        try:
            result: dict = gbif.Species.get(match_species['usageKey'])
        except KeyError:
            return []
        rank_index = [
            i for i, rank in enumerate(GBIF_RANKS)
            if rank in result.keys() and
                result['parent'] == result[rank]][0] + 1
        rank = GBIF_RANKS[rank_index]

        is_valid = result["taxonomicStatus"] == "ACCEPTED"

        classification_srids = [
                    result[f'{k}Key'] for k in GBIF_RANKS if k in result.keys()]

        out = []
        if not is_valid:
            out_kwargs = {
                "source_id": GBIF_SOURCE_KEY,
                "source_name": GBIF_SOURCE_NAME,
                "source_record_id": result["key"],
                "scientific_name": result["canonicalName"],
                "authorship": find_authorship(
                    result["canonicalName"],
                    result["scientificName"]),
                "rank": result['rank'].lower(),
                "classification_srids": classification_srids,
                "valid": is_valid,
                "valid_srid": result["acceptedKey"],
                "match_type": match_species["matchType"].lower(),
                "is_parent": False
            }
            out.append(cls(**out_kwargs))
        for rank_order, rank in enumerate(GBIF_RANKS):
            if rank not in result.keys():
                break
            taxa = result[rank]
            srid = result[rank + 'Key']
            match_type = None
            if rank == result["rank"].lower():
                valid_authorship = find_authorship(
                    result["canonicalName"],
                    result["scientificName"])
                is_parent = False
                if is_valid:
                    match_type = match_species["matchType"].lower()
            else:
                valid_authorship = None
                is_parent = True
            out_kwargs = {
                    "source_id": GBIF_SOURCE_KEY,
                    "source_record_id": srid,
                    "source_name": GBIF_SOURCE_NAME,
                    "scientific_name": taxa,
                    "authorship": valid_authorship,
                    "rank": rank,
                    "rank_order": rank_order,
                    "classification_srids":classification_srids[:rank_order + 1],
                    "valid": True,
                    "valid_srid": srid,
                    "match_type": match_type,
                    "is_parent": is_parent
                }
            out.append(cls(**out_kwargs))
        return out

    @classmethod
    def from_all_sources(cls, name: str, authorship: str = None):
        out = cls.from_global_names(name, authorship)
        out.extend(cls.from_gbif(name, authorship))
        return out


def find_authorship(name, name_simple):
    authorship = name.replace(name_simple, '')
    authorship = authorship.strip()
    try:
        if authorship[0] == '(' and authorship[-1] == ')' \
                and authorship.count('(') <= 1:
            authorship = authorship.lstrip('(').rstrip(')')
    except IndexError:
        pass
    return authorship
