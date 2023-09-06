import urllib.request
import json

BASE_URL = "https://www.wikidata.org/w/api.php?"

def search_entities(query, language="en"):
    """
    Search for entities on Wikidata based on a query.

    Args:
    - query (str): The search term.
    - language (str, optional): The language to search in. Default is English ('en').

    Returns:
    - dict: Search results as a dictionary.
    """
    
    params = {
        "action": "wbsearchentities",
        "search": query,
        "language": language,
        "format": "json",
        "type": "item"
    }
    
    url = BASE_URL + urllib.parse.urlencode(params)
    response = urllib.request.urlopen(url).read()
    data = json.loads(response)

    # Raise an exception if the request was not successful
    if "error" in data:
        raise Exception(data["error"]["info"])
    
    # Return search results
    results = data["search"]
    
    return results

def get_entities(id, languages=["en, fr"]):
    """
    Get details of a specific entity from Wikidata based on its QID.

    Args:
    - id (str): The identifier of the entity (e.g., Q12345).
    - languages (list, optional): List of languages to fetch details in. Default is ['en'].

    Returns:
    - dict: Entity details as a dictionary.
    """
    
    params = {
        "action": "wbgetentities",
        "ids": id,
        "languages": "|".join(languages),
        "format": "json"
    }
    
    url = BASE_URL + urllib.parse.urlencode(params)
    response = urllib.request.urlopen(url).read()
    data = json.loads(response)

    # Raise an exception if the request was not successful
    if "error" in data:
        raise Exception(data["error"]["info"])
    
    # Return entity details

    entity = data["entities"][id]

    return entity