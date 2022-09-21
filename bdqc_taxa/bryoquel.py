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

DB_FILE = 'bryoquel.sqlite'
db_path = pkg_resources.resource_filename('bdqc_taxa', DB_FILE)

# Connect to the database
conn = sqlite3.connect(db_path)

def match_species(species) -> dict:
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
        - clade: Clade
        - family_scientific_name: Famille
        - species_canonical_name: Noms latins acceptés
        - species_scientific_name: Noms latins acceptés, sans auteur
        - authorship: Auteur obtenu de Noms latins acceptés
        - vernacular_name_fr: Noms français acceptés
        - vernacular_name_en: Noms anglais acceptés
    """
    # Get the cursor
    c = conn.cursor()
    
    # Get the species name
    species = species.strip()
    
    # Fuzzy match the species name
    c.execute("SELECT * FROM bryoquel WHERE species_canonical_name LIKE ?", ('%' + species + '%',))
    rows = c.fetchall()

    # If there is a match, return the result
    if len(rows) == 1:
        return {
            'id': rows[0][0],
            'clade': rows[0][1],
            'family_scientific_name': rows[0][2],
            'species_canonical_name': rows[0][3],
            'species_scientific_name': rows[0][4],
            'authorship': rows[0][5],
            'vernacular_name_fr': rows[0][6],
            'vernacular_name_en': rows[0][7]
        }
    # If there is no match, return None
    elif len(rows) == 0:
        return None