# user-analysis of the LifeWatch project


Yearly analysis of the LifeWatch users since the start of the [LifeWatch project](https://lifewatch.be) (2012).

LW Users are identified through:

- authors of LifeWatch publications based on LW data
- users of the LW data systems (where possible)


### LifeWatch publications

LW publications consist of:

1. scientific articles (both peer and non-peer reviewed) 
2. monographs (books, rapports, proceedings and abstracts, theses)


(In order to be considered a LifeWatch publications, articles are manually analysed and collected in one of 11 LW special collections in IMIS.)

### Data systems

LW data systems taken into account for the user analysis are:

- [Marine Regions](https://marineregions.org)
- [WoRMS](https://marinespecies.org)
- data requests (via mail)

besides single data systems, users are also identified through:

- mailing lists
- registered users
- workshop participants 




The structure of the repository is as follows:

## Data

./publication_data/ --> data on the lifewatch publications, exported from IMIS (either as one large export or split per year) 
./reference_Data/ --> standardized data (e.g. affiliation names, country, quadruple helix terms, institute type names, ... )
./wos_export/ --> data on lifewatch publications with a WoS code, exported from Web Of Science

## Tools

The tools used in various steps of the user analysis.

lw_pub_statistics --> to standardize publication data, see ./lw_pub_statistics/README.md on how to use 




 
