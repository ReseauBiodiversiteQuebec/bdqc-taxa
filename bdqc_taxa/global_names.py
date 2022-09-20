from urllib.request import Request, urlopen, URLError, HTTPError
from urllib.parse import urlencode, quote_plus
import json

__all__ = ['verify']

VERIFY_PREFIX = "api/v1/verifications"
HOST = "https://verifier.globalnames.org"

DATA_SOURCES = [1, 3, 147]

ALL_MATCHES = True


def verify(name: str, data_sources: list = DATA_SOURCES, all_matches: bool = ALL_MATCHES) -> dict:
    # Format python bool to json bool
    if all_matches:
        all_matches = "true"
    else:
        all_matches = "false"

    path_name = quote_plus(name.lower())


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
