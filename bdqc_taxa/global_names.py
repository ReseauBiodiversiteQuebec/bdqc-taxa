from urllib.request import Request, urlopen, URLError, HTTPError
from urllib.parse import urlencode, quote_plus
from typing import List
import json

__all__ = ['verify']

VERIFY_PREFIX = "api/v1/verifications"
HOST = "https://verifier.globalnames.org"

DATA_SOURCES = [1, 3, 147]

ALL_MATCHES = True


def _verify(name: str, data_sources: list = DATA_SOURCES, all_matches: bool = ALL_MATCHES) -> dict:
    # Format python bool to json bool
    if all_matches:
        all_matches = "true"
    else:
        all_matches = "false"

    path_name = quote_plus(name)


    params = urlencode(
        {'capitalize': "true",
         'all_matches': all_matches,
         'data_sources': "|".join(['%.0f' % v for v in data_sources])
         }
    )


    req = Request(
        url="/".join([HOST, VERIFY_PREFIX, path_name]) + "?" + params,
        headers={"Content-Type": "application/json"}
    )
    try:
        data = urlopen(req)
    except HTTPError as e:
        return e
    except URLError as e:
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e, 'code'):
            return e.code
        else:
            return e
    else:
        try:
            out = json.loads(data.read().decode('utf-8'))
            return out
        except KeyError:
            return [None]

def _solve_source_name_conflicts(results: List[dict]) -> List[dict]:
    """
    This function takes a list of results from the global names verifier and returns a list of results with conflicts solved.
    :param results: A list of results from the global names verifier.
    :return: A list of results with conflicts solved.
    """
    # First, we need to identify the conflicts
    unique_results = {}
    for result in results:
        key = str(result['dataSourceId']) + result['matchedCanonicalFull']
        try:
            unique_results[key].append(result)
        except KeyError:
            unique_results[key] = [result]

    # Now we need to solve the conflicts
    out = []
    for name_result in unique_results.values():
        if len(name_result) == 1:
            out.extend(name_result)
        else:
            if any([result['isSynonym'] is False for result in name_result]):
                out.extend([result for result in name_result if result['isSynonym'] is False])
            else:
                out.extend(name_result)
    return out

def verify(name: List[str], data_sources: list = DATA_SOURCES, all_matches: bool = ALL_MATCHES) -> List[dict]:
    """
    This function takes a list of names and returns a list of results from the global names verifier.
    :param names: A list of names to verify.
    :param data_sources: A list of data sources to use.
    :param all_matches: Whether to return all matches.
    :return: A list of results from the global names verifier.
    """
    gn_out = _verify(name, data_sources, all_matches)
    names = gn_out['names']
    for i, name in enumerate(names):
        try:
            names[i]['results'] = _solve_source_name_conflicts(name['results'])
        except KeyError:
            pass
    return gn_out