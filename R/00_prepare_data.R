library(readxl)
library(dplyr)
library(stringr)

# Script to count the number of times that a keyword appears in the abstract of a paper

# Read table with title, keywords and abstracts
publications <- read_excel("publication_data/lifewatch_pubs_20211004.xlsx")

# Remove abstracts that are empty and duplicated 
abstracts <- publications %>%
  select(BrefID, StandardTitle, AbstractEnglish) %>%
  filter(AbstractEnglish != "NULL") %>%
  filter(!duplicated(BrefID))

# Count n times a certain string appears
abstracts <- abstracts %>%
  mutate(n_oil_spill = str_count(AbstractEnglish, "oil spill")) %>%
  arrange(desc(n_oil_spill)) %>%
  filter(n_oil_spill > 0)

# Visualize
abstracts
#> # A tibble: 10 x 4
#> BrefID StandardTitle                    AbstractEnglish                   n_oil_spill
#> <dbl> <chr>                            <chr>                                   <int>
#> 1 312940 Effect of crude oil exposure an~ Dispersant application is used a~           2
#> 2 243003 Analyses of sublittoral macrobe~ Sublittoral macrobenthic communi~           1
#> 3 245313 Migration, foraging, and reside~ Northern Gulf of Mexico (NGoM) l~           1
#> 4 282303 Toxicities of oils, dispersants~ Phytotoxicity results are review~           1
#> 5 288034 Effects of crude oil exposure o~ Gelatinous zooplankton play an i~           1
#> 6 291006 A review of the empirical liter~ The need to carry out monitoring~           1
#> 7 301034 Effects of acute exposure to di~ The present study investigates t~           1
#> 8 305171 Response of natural phytoplankt~ During the 2010 Deepwater Horizo~           1
#> 9 319802 Global assessment of marine bio~ Increasing global energy demands~           1
#> 10 319996 Dataset showing the abundance a~ This dataset supports the paper ~           1





# This turns the abstracts into single words
# library(tidytext)
# # Tokenize one publication
# abstracts[1,]
# #> 215501
# 
# abstract_n <- abstracts %>%
#   filter(BrefID == 215501) %>%
#   unnest_tokens(tokenized_abstract, AbstractEnglish, "words")
# 
# 
# "ngrams"
# head(abstract_n$tokenized_abstract)
# # [1] "with the completion"           "the completion of"            
# # [3] "completion of a"               "of a single"                  
# # [5] "a single unified"              "single unified classification"