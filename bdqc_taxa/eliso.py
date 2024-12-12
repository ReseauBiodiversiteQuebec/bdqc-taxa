#====================================================================================================
# Match taxa in eliso's taxonomy from custom_source sqlite database
#
# Victor Cameron
# 2024-04-23
#
# The eliso_invertebrates table has the following columns:
# taxa_name: Scientific name of the taxon
# vernacular_fr: French vernacular name of the taxon
# taxa_rank: Taxon rank
# Embranchement: Phylum
# Classe: Class
# Ordre: Order
# Famille: Family
# Genre: Genus
# Espèce: Species
#====================================================================================================


import sqlite3
import importlib.resources

# Get the database file from the package data

DB_FILE = 'custom_sources.sqlite'
with importlib.resources.open_binary('bdqc_taxa', DB_FILE) as db_file:
    db_path = db_file.name

# Connect to the database
conn = sqlite3.connect(db_path)

def match_taxa(name) -> dict:
    """Match a species name to Eliso's invertebrate database
    Parameters
    ----------
    name : str

    Returns
    -------
    dict
        A dictionary with the following keys:
        taxa_name: Scientific name of the taxon
        vernacular_fr: French vernacular name of the taxon
        taxa_rank: Taxon rank
        Embranchement: Phylum
        Classe: Class
        Ordre: Order
        Famille: Family
        Genre: Genus
        Espèce: Species
        
    """

    # Get the cursor
    c = conn.cursor()

    # Get the species name
    name = name.strip()
    
    c.execute('''
    SELECT * FROM eliso_invertebrates
    WHERE taxa_name = ?
    ORDER BY taxa_rank
    ''', (name,))

    # Get the first result
    result = c.fetchone()

    # Close the cursor
    c.close()


    # If there is a match, return the result
    if result:
        return {
            'taxa_name': result[0],
            'vernacular_fr': result[1],
            'taxa_rank': result[2],
            'Embranchement': result[3],
            'Classe': result[4],
            'Ordre': result[5],
            'Famille': result[6],
            'Genre': result[7],
            'Espèce': result[8]
        }
    # If there is no match, return None
    else:
        return None