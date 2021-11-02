from . import global_names
from typing import List
from inspect import signature


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
                 match_type: str = ''):
        for param in signature(self.__init__).parameters:
            setattr(self, param, eval(param))

    @classmethod
    def from_global_names(cls, name: str, authorship: str = None):
        if isinstance(authorship, str) and authorship.strip():
            name =" ".join([name, authorship])

        gn_results = global_names.verify(name)
        gn_results = [
            result for species in gn_results 
            for result in species['preferredResults']]
        for result in gn_results:
            is_valid = result["currentRecordId"] == result["recordId"]
            out = []
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
                    "match_type": result["matchType"].lower()
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
                    if is_valid:
                        match_type = result["matchType"].lower()
                else:
                    valid_authorship = None
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
                        "match_type": match_type
                    }
                out.append(cls(**out_kwargs))
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
