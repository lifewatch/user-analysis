# lw_pub_statistics

A python module to standardize data of lifewatch publications, exported from IMIS.

# How to use

```
# create a py virtualenv

# build the module

# help
lw_pub_statistics --help

# run it
python -mlw_pub_statistics --publicationData ../publication_data/ --referenceData ../reference_data/ --wosExportData ../wos_export/

```

### Input parameters:

publicationData --> Specifies the folder with publication data
(Note: please provide the IMIS query with the export data; so the publication_data folder can be updated with correctly structured data.)
referenceData --> Specifies the folder with standardized data
wosExportData --> Specifies the folder with export data from Web of Science (from publication with a WoS code)