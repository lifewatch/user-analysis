library(readxl)
library(dplyr)
library(stringr)

# Script to count the number of times that a keyword appears in the abstract of a paper

# Read table with title, keywords and abstracts
publications <- read_excel("publication_data/lifewatch_pubs_20211004.xlsx")


# Remove abstracts that are empty and duplicated
publications_SDG <- publications %>%
  select(BrefID, StandardTitle, AbstractEnglish, ThesTerms, TaxTerms, OtherTerms) %>%
  filter(AbstractEnglish != "NULL") %>%
  filter(!duplicated(BrefID)) %>%
  # slice_head(n = 50) %>% #delete to process all publications
  mutate(SDG1 = FALSE,
         SDG2 = FALSE,
         string = paste(StandardTitle,
                        AbstractEnglish,
                        ThesTerms,
                        TaxTerms,
                        OtherTerms,
                        sep = " ")
  )



# Function to check if all items from 'terms' are present in 'string' (abstract)
# for all the list terms, check if ALL subitems are in the abstract
# if there is one term in the list, this returns TRUE if present
# if there are two terms both have to be present before returning TRUE
check_all_present <- function(terms, string){all(str_detect(string, terms))}


# Define all SDG Terms in a list, a vector of items means both need to be present

# # read queries
# queries <- read_excel("SDG_queries/input_queries/SDG_queries_collated_20191010.xlsx")
#
#
# # helper lines to extract terms from queries
# SDG1_Q <- queries$Query[3]
# SDG1_Q <- SDG1_Q  %>%
#   str_replace_all("\\{", "'") %>%  # replace bracket by quote
#   str_replace_all("\\}", "'") %>%  # replace bracket by quote
#   str_replace_all("\\s{2,}", " ") %>% # remove double or triple spaces
#   str_remove_all("^TITLE-ABS-KEY\\s\\(\\s\\(") %>% # remove initial "TITLE-ABS-KEY ( ("
#   str_remove_all("\\s\\)\\s\\)$") # remove trailing " ) )"

    # SDG1 terms as a list
    terms_SDG1 <- list("extreme poverty",
               "poverty alleviation",
               "poverty eradication",
               "poverty reduction",
               "international poverty line",
               "financial empowerment",
               "distributional effect",
               "distributional effects",
               "child labor",
               "child labour",
               "development aid",
               "social protection",
               "social protection system",
               "microfinanc",
               "micro-financ",
               "resilience of the poor",
               "food bank",
               "food banks",
               # if multiple terms, both need to be present
               c("financial aid", "poverty"),
               c("financial aid", "poor"),
               c("financial aid", "north-south divide"),
               c("financial development", "poverty"),
               c("social protection", "access"),
               c("safety net", "poor"),
               c("safety net", "vulnerable"),
               c("economic resource", "access"),
               c("economic resources", "access")
               )

    # SDG2 terms as a list
    terms_SDG2 <- list("land tenure rights",
                       c("smallholder", "farm"),
                       c("smallholder", "forestry"),
                       c("smallholder", "pastoral"),
                       c("smallholder", "agriculture"),
                       c("smallholder", "fishery"),
                       c("smallholder", "food producer"),
                       c("smallholder", "food producers"),
                       "malnourish",
                       "malnutrition",
                       "undernourish*",
                       "undernutrition",
                       "agricultural production",
                       "agricultural productivity",
                       "agricultural practices",
                       "agricultural management",
                       "food production",
                       "food productivity",
                       "food security",
                       "food insecurity",
                       "land right",
                       "land rights",
                       "land reform",
                       "land reforms",
                       "resilient agricultural practices",
                       c("agriculture", "potassium"),
                       "fertilizer",
                       "fertiliser",
                       "food nutrition improvement",
                       "hidden hunger",
                       "genetically modified food",
                       c("gmo", "food" ),
                       "agroforestry practices",
                       "agroforestry management",
                       "agricultural innovation",
                       c("food security", "genetic diversity"),
                       c("food market", "restriction"),
                       c("food market", "tariff"),
                       c("food market", "access"),
                       c("food market", "north south divide"),
                       c("food market", "development governance"),
                       "food governance",
                       "food supply chain",
                       "food value chain")
                        # special case below, is done separately:
                       # c("food commodity market", AND NOT "disease")

    #SDG 3 terms as a list
    # still to do
    terms_SDGs3 <- list(" ( human AND ( health* OR disease* OR illness* OR medicine* OR mortality ) ) OR 'battered child syndrome' OR 'cardiovascular disease' OR 'cardiovascular diseases' OR 'chagas' OR 'child abuse' OR 'child neglect' OR 'child well-being index' OR 'youth well-being index' OR 'child wellbeing index' OR 'youth wellbeing index' OR 'water-borne disease' OR 'water-borne diseases' OR 'water borne disease' OR 'water borne diseases' OR 'tropical disease' OR 'tropical diseases' OR 'chronic respiratory disease' OR 'chronic respiratory diseases' OR 'infectious disease' OR 'infectious diseases' OR 'sexually-transmitted disease' OR 'sexually transmitted disease' OR 'sexually-transmitted diseases' OR 'sexually transmitted diseases' OR 'communicable disease' OR 'communicable diseases' OR aids OR hiv OR 'human immunodeficiency virus' OR tuberculosis OR malaria OR hepatitis OR polio* OR vaccin* OR cancer* OR diabet* OR 'maternal mortality' OR 'child mortality' OR 'childbirth complications' OR 'neonatal mortality' OR 'neo-natal mortality' OR 'premature mortality' OR 'infant mortality' OR 'quality adjusted life year' OR 'maternal health' OR 'preventable death' OR 'preventable deaths' OR 'tobacco control' OR 'substance abuse' OR 'drug abuse' OR 'tobacco use' OR 'alcohol use' OR 'substance addiction' OR 'drug addiction' OR 'tobacco addiction' OR alcoholism OR suicid* OR 'postnatal depression' OR 'post-natal depression' OR 'zika virus' OR dengue OR schistosomiasis OR 'sleeping sickness' OR ebola OR 'mental health' OR 'mental disorder' OR 'mental illness' OR 'mental illnesses' OR 'measles' OR 'neglected disease' OR 'neglected diseases' OR diarrhea OR diarrhoea OR cholera OR dysentery OR 'typhoid fever' OR 'traffic accident' OR 'traffic accidents' OR 'healthy lifestyle' OR 'life expectancy' OR 'life expectancies' OR 'health policy' OR ( 'health system' AND ( access OR accessible ) ) OR 'health risk' OR 'health risks' OR 'inclusive health' OR obesity OR 'social determinants of health' OR 'psychological harm' OR 'psychological wellbeing' OR 'psychological well-being' OR 'psychological well being' OR 'public health'"
                        )

# loop or apply to all publications
for (i in seq(1:nrow(publications_SDG))){
      print(i)

    #loop or apply to all SDGs
      # SDG1
      all_list <- lapply(terms_SDG1, check_all_present, publications_SDG$string[i])
      # TRUE if any of the list is TRUE
      if (any(unlist(all_list))){publications_SDG$SDG1[i] <- TRUE}

      #SDG2
      all_list <- lapply(terms_SDG2, check_all_present, publications_SDG$string[i])
      # TRUE if any of the list is TRUE
      if (any(unlist(all_list))){publications_SDG$SDG2[i] <- TRUE}
      # special case: "food commodity market", AND NOT "disease"
      if (str_detect(publications_SDG$string[i], "food commodity market") &
          !str_detect(publications_SDG$string[i], "disease")) {publications_SDG$SDG2[i] <- TRUE}
      
      #SDG3 ...

} # next publication


#drop string column for writing to csv
publications_SDG_csv <- publications_SDG %>%
  select(-string)

write.csv(publications_SDG_csv,
          file = "SDG_queries/publications_SDG1_SDG2.csv",
          row.names = FALSE)
