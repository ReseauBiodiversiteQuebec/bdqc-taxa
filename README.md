# BDQC-TAXA

`bdqc_taxa` is a python package that interface with *Biodiversité Québec*'s database to query reference taxa sources, parse their return and generate records.


## Installation

> **For installation in postgres server**
> 
> Installation must be performed as `postgres` user :
> ```
> sudo su postgres
> pip install ...
> ```

For a new installation

```
pip install git+https://github.com/ReseauBiodiversiteQuebec/bdqc_taxa#egg=bdqc_taxa
```

For an upgrade
```
pip install --upgrade git+https://github.com/ReseauBiodiversiteQuebec/bdqc_taxa#egg=bdqc_taxa
```

## Usage

### Match a scientific name against all sources

The `taxa_ref` module is used to query the reference taxa sources and parse their return using fuzzy matching.

For a specific match, the module provides functions to return scientific name, taxonomic hierarchy, vernacular name and source of the match. For each source, valid scientific names are returned as well as synonyms when corresponding to the matched input name. Parent taxa are returned as well as children taxa when corresponding to the matched input name.

### Example

Query for all sources using a scientific name can be done with the following method. This should fits most use cases.

```python
from bdqc_taxa.taxa_ref import TaxaRef

results = TaxaRef.from_all_sources('Canis lupus')
```

### Complex names

When the taxon related to an observation is complex, such as multiple organism are identified for the same observation(Species 1 | Species 2 | Species 3), a single observed taxonomic entry is injected as such. References will be obtained for each single organism listed by the complex and all related parents. References matched from complex observed taxons are identified as such and can then be included or discarded from queries performed by the user. Common parent taxon are identified as such and can be used to query complex observed taxons.


### Conflicts

Certain scientific names corresponds to different organism within two entirely different branches of the tree of life. For example, the scientific name *Salix* corresponds to the genus of willows in the plant kingdom and to a genus of tunicates in the animal kingdom. To avoid matching for such case, the user can specify a parent taxa name to restrict the results to the branch containing the parent taxa. For example, the user can specify the parent taxa name *Plantae* to restrict the results to the plant kingdom.

The `parent_taxa` argument is optional. If not specified, the module will return all results for the given scientific name.

```python
from bdqc_taxa.taxa_ref import TaxaRef

results = TaxaRef.from_all_sources('Salix', parent_taxa='Plantae')
```


## Find vernacular names for a scientific name

The `taxa_vernacular` module is used to query the reference taxa sources and parse their return using fuzzy matching in english and french.

For a specific match, the module provides functions to return the accepted vernacular names in english and french. The rank order of the sources is used to determine the accepted vernacular name.

### Example

Query for all sources using a scientific name can be done with the following method. This should fits most use cases.

```python
from bdqc_taxa.vernacular import Vernacular

results = Vernacular.from_match('Canis lupus')
```

### Synonyms

For certain sources, such as CDPNQ, the vernacular name will be returned for accepted synonyms. If observed scientific name differs, the user should do multiple queries for each known synonyms.


## Sources

* Global Names Resolver (GNR) : Retrieve the scientific name and the taxonomic hierarchy of a given name against many sources. Selected sources are VASCAN, ITIS and COL. Query is performed against the GNR API.
* GBIF : Retrieve the scientific name and the taxonomic hierarchy of a given name against the GBIF backbone taxonomy. Query is performed against the GBIF API.
* Bryoquel : Implemented by the *Biodiversité Québec* team, this source is used to retrieve the scientific name and the taxonomic hierarchy of a given name against the Bryophytes of Québec. Query is performed against the the `custom_sources` sqlite database implemented by the *Biodiversité Québec* team using the Bryoquel excel file. See below for more details.
* CDPNQ : Implemented by the *Biodiversité Québec* team, this source is used to retrieve the scientific name and the taxonomic hierarchy of a given name against the list for the *Centre de données sur le patrimoine naturel du Québec*. Query is performed against the the `custom_sources` sqlite database implemented by the *Biodiversité Québec* team using the CDPNQ excel files. See below for more details.
* Wikidata : Retrieve the vernacular name of a given scientific name against Wikidata. Query is performed against the Wikidata API.

### Modules

Wrapper functions to query the sources using either api or the sqlite database are individually implemented in modules `gbif`, `global_names`, `bryoquel`, `cdpnq` and `wikidata`. 


## Custom sources

These tables containts the custom sources used by the `taxa_ref` module. They are implemented in the `custom_sources` sqlite database. The database is located in the `bdqc_taxa` package directory. Full-text search is implemented for the sqlite database using the `FTS5` extension. 

### TABLE bryoquel

#### Description: 
    This file was generated on 2022-09-21 from the Bryoquel taxonomy file.
    The file was downloaded from http://societequebecoisedebryologie.org/Bryoquel.html on 2022-09-21.
    The last version of the bryoquel xlsx file is from 2022-09-12`.
    The file was parsed using the script `scripts/parse_bryoquel.py`.
    The file was parsed using the script parse_bryoquel.ipynb.

#### Columns:
    The file contains a pandas dataframe with the following columns:
    id: the Bryoquel IDtaxon
    scientific_name: Noms latins acceptés du taxon, sans auteur
    taxon_rank: Taxon rank
    genus: Taxon genus
    family: Taxon family
    clade: Taxon clade
    canonical_full: Noms latins acceptés du taxon, avec auteur
    authorship: Auteur obtenu de Noms latins acceptés
    vernacular_name_fr: Noms français acceptés
    vernacular_name_en: Noms anglais acceptés


### TABLE cdpnq_odonates

#### Description: 
    This file was generated from the CDPNQ odonates data file.
    The file was obtained from Anouk.Simard@mffp.gouv.qc.ca on May 24, 2022
    The last version of the bryoquel xlsx file is from 2022-09-12`.
    The file was parsed using the script `scripts/make_cdpnq_odonates.py`.

#### Columns:
    name: scientific name
    valid_name: valid scientific name
    rank: rank of the taxa
    synonym: boolean indicating if the name is a synonym
    author: author of the scientific name
    canonical_full: canonical full name
    vernacular_fr: vernacular name in French
    vernacular_fr2: vernacular name in French from Natureserve


### TABLE cdpnq_vertebrates

#### Description: 
    This file was generated from the Liste de la faune vert�br�e du Qu�bec (LFVQ) Data file LFVQ_05_12_2022.xlsx 
    The file was obtained from Donn�es Qu�bec on 2023-01-12.
    The last version of thefile is from 2022-12-05`.
    The file was parsed using the script `scripts/make_cdpnq_vertebrates.py`.

#### Columns:
    name: scientific name
    valid_name: valid scientific name
    rank: rank of the taxa
    synonym: boolean indicating if the name is a synonym
    author: author of the scientific name
    canonical_full: canonical full name
    vernacular_fr: vernacular name in French
    vernacular_en: vernacular name in English

Notes:
    The entries have no recorded author.
