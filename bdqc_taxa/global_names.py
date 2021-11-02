from urllib.request import Request, urlopen, URLError, HTTPError
from urllib.parse import urlencode, quote_plus
import json

__all__ = ['verify']

VERIFY_PREFIX = "api/v1/verifications"
HOST = "https://verifier.globalnames.org"


def verify(name: str):
    path_name = quote_plus(name.lower())
    params = urlencode(
        {'pref_sources': "|".join(['%.0f' % v for v in [1, 3, 11, 147]]),
         'capitalize': "true"}
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
