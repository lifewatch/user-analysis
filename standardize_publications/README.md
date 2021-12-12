# standardize_publications

A python module to standardize information of the lifewatch publications.


# How to use

```
# create and activate a virtualenv 

# install dependencies 
make init

# help (for all available parameters)
python -mstandardize_publications --help

# run it for publications
python -mstandardize_publications -i ../LW_publications/name-of-input-file -sl ../reference_data/Affiliations_standardized.csv -si ../reference_data/Affiliations_info.xlsx -wd ../wos_export/ -o ../LW_publications_standardized/name-of-output-file

# run it for data-systems
python -mstandardize_publications -i ../LW_data_systems/name-of-input-file -sl ../reference_data/Affiliations_standardized.csv -si ../reference_data/Affiliations_info.xlsx -wd ../wos_export/ -o ../LW_data_systems_standardized/name-of-output-file

```
