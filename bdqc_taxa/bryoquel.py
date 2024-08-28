# Match species in the Bryoquel sqlite database

# The bryoquel table has the following columns:
# id: the Bryoquel IDtaxon
# family_scientific_name: Famille
# species_scientific_name: Noms latins accept�s
# vernacular_name_fr: Noms fran�ais accept�s
# vernacular_name_en: Noms anglais accept�s
# clade: Clade
# authorship: Auteur obtenu de Noms latins accept�s


import sqlite3
import pkg_resources

# Get the database file from the package data

DB_FILE = 'custom_sources.sqlite'
db_path = pkg_resources.resource_filename('bdqc_taxa', DB_FILE)

# Connect to the database
conn = sqlite3.connect(db_path)

def match_taxa(species) -> dict:
    """Match a species name to the Bryoquel database
    
    Parameters
    ----------
    species : str
        The species name to match
    
    Returns
    -------
    dict
        A dictionary with the following keys:
        - id: the Bryoquel IDtaxon
        - scientific_name: Noms latins accept�s du taxon, sans auteur
        - taxon_rank: Taxon rank
        - genus: Taxon genus
        - family: Taxon family
        - clade: Taxon clade
        - canonical_full: Noms latins accept�s du taxon, avec auteur
        - authorship: Auteur obtenu de Noms latins accept�s
        - vernacular_name_fr: Noms fran�ais accept�s
        - vernacular_name_en: Noms anglais accept�s
    """
    # Get the cursor
    c = conn.cursor()
    
    # Get the species name
    species = species.strip()

    c.execute('''
    SELECT bryoquel.* FROM bryoquel
    JOIN bryoquel_fts ON bryoquel_fts.scientific_name = bryoquel.scientific_name
    WHERE bryoquel_fts.scientific_name MATCH ?
    ORDER BY rank
    LIMIT 1
    ''', (f'"{species}"',))

    rows = c.fetchone()

    # If there is a match, return the result
    if rows:
        return {
            'db_id': rows[0],
            'id': rows[1],
            'scientific_name': rows[2],
            'taxon_rank': rows[3],
            'genus': rows[4],
            'family': rows[5],
            'clade': rows[6],
            'canonical_full': rows[7],
            'authorship': rows[8],
            'vernacular_name_fr': rows[9],
            'vernacular_name_en': rows[10]
        }
    # If there is no match, return None
    else:
        return None
    

def match_taxa_exact(species) -> dict:
    """Match *exactly* a species name to the Bryoquel database
    
    Parameters
    ----------
    species : str
        The species name to match
    
    Returns
    -------
    dict
        A dictionary with the following keys:
        - id: the Bryoquel IDtaxon
        - scientific_name: Noms latins accept�s du taxon, sans auteur
        - taxon_rank: Taxon rank
        - genus: Taxon genus
        - family: Taxon family
        - clade: Taxon clade
        - canonical_full: Noms latins accept�s du taxon, avec auteur
        - authorship: Auteur obtenu de Noms latins accept�s
        - vernacular_name_fr: Noms fran�ais accept�s
        - vernacular_name_en: Noms anglais accept�s
    """
    # Get the cursor
    c = conn.cursor()
    
    # Get the species name
    species = species.strip()

    c.execute('''
    SELECT * FROM bryoquel
    WHERE scientific_name = ?
    ORDER BY taxon_rank
    LIMIT 1
    ''', (species,))

    rows = c.fetchone()

    # If there is a match, return the result
    if rows:
        return {
            'db_id': rows[0],
            'id': rows[1],
            'scientific_name': rows[2],
            'taxon_rank': rows[3],
            'genus': rows[4],
            'family': rows[5],
            'clade': rows[6],
            'canonical_full': rows[7],
            'authorship': rows[8],
            'vernacular_name_fr': rows[9],
            'vernacular_name_en': rows[10]
        }
    # If there is no match, return None
    else:
        return None