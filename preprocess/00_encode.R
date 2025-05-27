library(data.table)
library(tidyverse)

persoontab <- fread("./data/raw/persoon_tab_250k.csv")

country_codes <- fread("./data/raw/country_codes.csv")
country_codes$Code <- str_pad(country_codes$Code, 4, "left", "0")

## GBAGEBOORTELAND / GBAGEBOORTELANDMOEDER / GBAGEBOORTELANDVADER
## GBAGESLACHT / GBAGESLACHTVADER / GBAGESLACHTMOEDER

coded_list <- setNames(country_codes$Land,
                       country_codes$Code)

persoontab[, GBAGEBOORTELAND := coded_list[as.character(GBAGEBOORTELAND)]]
persoontab[, GBAGEBOORTELANDMOEDER := coded_list[as.character(GBAGEBOORTELANDMOEDER)]]
persoontab[, GBAGEBOORTELANDVADER := coded_list[as.character(GBAGEBOORTELANDVADER)]]
persoontab[, GBAHERKOMSTGROEPERING := coded_list[as.character(GBAHERKOMSTGROEPERING)]]

coded_list <- setNames(c("Male", "Female"), c("1", "2"))

persoontab[, GBAGESLACHT := coded_list[as.character(GBAGESLACHT)]]
persoontab[, GBAGESLACHTMOEDER := coded_list[as.character(GBAGESLACHTMOEDER)]]
persoontab[, GBAGESLACHTVADER := coded_list[as.character(GBAGESLACHTVADER)]]

fwrite(persoontab, "./data/raw/persoon_tab_250k_coded.csv")
