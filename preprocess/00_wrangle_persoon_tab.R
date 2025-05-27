library(data.table)
library(glue)
library(tidyverse)

holdout <- T

persoon_path <- "G:/Bevolking/GBAPERSOONTAB/2020/geconverteerde data/GBAPERSOON2020TABV3.csv"

persoon_tab <- fread(persoon_path)

country_codes <- fread("./data/raw/country_codes.csv")
country_codes$Code <- str_pad(country_codes$Code, 4, "left", "0")

coded_list <- setNames(country_codes$Land,
                       country_codes$Code)

persoon_tab[, GBAGEBOORTELAND := coded_list[as.character(GBAGEBOORTELAND)]]
persoon_tab[, GBAGEBOORTELANDMOEDER := coded_list[as.character(GBAGEBOORTELANDMOEDER)]]
persoon_tab[, GBAGEBOORTELANDVADER := coded_list[as.character(GBAGEBOORTELANDVADER)]]
persoon_tab[, GBAHERKOMSTGROEPERING := coded_list[as.character(GBAHERKOMSTGROEPERING)]]

coded_list <- setNames(c("Male", "Female"), c("1", "2"))

persoon_tab[, GBAGESLACHT := coded_list[as.character(GBAGESLACHT)]]
persoon_tab[, GBAGESLACHTMOEDER := coded_list[as.character(GBAGESLACHTMOEDER)]]
persoon_tab[, GBAGESLACHTVADER := coded_list[as.character(GBAGESLACHTVADER)]]

for (n in c(250000, 500000, 1000000, 0)) {
  if (n == 0) {
    k <- ""
  } else if (holdout) {
    k <- "_holdout"
  } else {
    k <- paste0("_", round(n / 1000), "k")
  }
  
  in_file <- glue("./data/raw/base_sample{k}.csv")
  base_sample <- fread(in_file)
  
  sample_table <- persoon_tab[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/persoon_tab{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
  
  if (holdout) {
    break
  }
}
