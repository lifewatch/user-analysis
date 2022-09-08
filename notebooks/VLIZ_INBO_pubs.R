# publications consortium

library(readxl)
library(dplyr)
library(stringr)



# Read table with all papers
publications <- read.csv(file.path("LW_publications_standardized","LWpubs_stand_all_SDG.csv"),
                         stringsAsFactors = FALSE,
                         encoding = 'UTF-8')


# Read list of LW employees
lw_employees <- read.csv(file.path("reference_data","LifeWatch_employees.csv"))

# Read list of LW in-kind contributions
lw_inkind <- read.csv(file.path("reference_data","LifeWatch_inkind.csv"))

# number of publications in this list:
npubs <- length(unique(publications$BrefID))
# 6223


# Select VLIZ and INBO pubs, remove duplicated BrefIDs
pubs_VLIZINBO <- publications %>%
  filter(Affiliation %in% c("Flanders Marine Institute", "VLIZ", "Research Institute for Nature and Forest", "INBO")) %>%
  filter(!duplicated(BrefID))
#74

# Select VLIZ and INBO pubs, remove duplicated BrefIDs
pubs_VLIZINBO_v2 <- publications %>%
  filter(str_detect(Affiliation,
                    "Flanders Marine Institute|VLIZ|vliz|Research Institute for Nature and Forest|INBO|inbo")) %>%
  filter(!duplicated(BrefID))
#151

# Select VLIZ and INBO pubs, remove duplicated BrefIDs
pubs_VLIZINBO_v3 <- publications %>%
  filter(str_detect(stand_affil,
                    "Flanders Marine Institute|VLIZ|vliz|Research Institute for Nature and Forest|INBO|inbo")) %>%
  filter(!duplicated(BrefID))
#168

# Select VLIZ and INBO pubs, remove duplicated BrefIDs
pubs_VLIZINBO_xls <- publications_xls %>%
  filter(str_detect(Affiliation,
                    "Flanders Marine Institute|VLIZ|vliz|Research Institute for Nature and Forest|INBO|inbo")) %>%
  filter(!duplicated(BrefID))



lw_employee_pattern <- paste(lw_employees$citation_format, collapse = "|")


pubs_LW_cons <- publications %>%
  filter(str_detect(RefStrFull,
                    lw_employee_pattern)) %>%
  filter(!duplicated(BrefID))
# 242

hist(pubs_LW_cons$Year)

table(pubs_LW_cons$DocType)
# Book chapters  Book/Monograph      Data paper        Ephemera
# 103              10              13              11
# Journal article         Reports
# 99               6

write.csv(pubs_LW_cons,
          file = file.path("LW_publications_standardized","LifeWatch_employee_papers.csv"),
          fileEncoding = 'UTF-8')


# inkind publications
lw_inkind_pattern <- paste(lw_inkind$citation_format, collapse = "|")


pubs_LW_inkind <- publications %>%
  filter(str_detect(RefStrFull,
                    lw_inkind_pattern)) %>%
  filter(!duplicated(BrefID))


# both in-kind and payroll
lw_both_pattern <- paste(lw_inkind_pattern, lw_employee_pattern, collapse = "|")

pubs_LW_both <- publications %>%
  filter(str_detect(RefStrFull,
                    lw_both_pattern)) %>%
  filter(!duplicated(BrefID))

hist(pubs_LW_both$Year)

table(pubs_LW_both$DocType)
# Book chapters  Book/Monograph      Data paper        Ephemera
# 112              15              13              11
# Journal article         Reports
# 120               8

write.csv(pubs_LW_both,
          file = file.path("LW_publications_standardized","LifeWatch_employee_inkind_papers.csv"),
          fileEncoding = 'UTF-8')
