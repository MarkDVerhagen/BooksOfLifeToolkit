library(data.table)
library(haven)
library(tidyverse)
library(glue)

sample_n <- c(250000, 500000, 1000000)

eval <- TRUE

# household_path <- "G:/Bevolking/GBAHUISHOUDENSBUS/geconverteerde data/GBAHUISHOUDENS2020BUSV1.csv"
# hh_bus <- fread(household_path)

# persoon_path <- "G:/Bevolking/GBAPERSOONTAB/2020/geconverteerde data/GBAPERSOON2020TABV3.csv"
train_path <- "H:/DATASETS/train.csv"

train_set <- fread(train_path)

# 200K eval
if (eval) {
  k <- 200
  seed_ossc <- fread(
    "H:/pmt/cruijff_runs/pmt_train_and_evaluation_samples_seed_1.csv")
  sample_table <- train_set[
    RINPERSOON %in% seed_ossc$RINPERSOON[seed_ossc$train_sample_n_200000 == 1]]
  
  write.csv(sample_table[, .(RINPERSOON, children_post2021)],
            glue("./bol_generation/data/raw/base_sample_{k}k.csv"))  
}


for (n in sample_n) {
  set.seed(1704)
  if (sample_n == 0) {
    sample_rins <- unique(persoon_tab_train$RINPERSOON)
  } else {
    sample_rins <- sample(persoon_tab_train$RINPERSOON, sample_n)  
  }
  k <- round(n / 1000)
  sample_table <- train_set[RINPERSOON %in% sample_rins, ]
  write.csv(sample_table[, .(RINPERSOON, children_post2021)],
            glue("./bol_generation/data/raw/base_sample_{k}k.csv"))
}

persoon_tab <- fread(persoon_path)
train_set <- fread(train_path)

## Add read on train set
persoon_tab <- persoon_tab[between(GBAGEBOORTEJAAR, 1975, 2002), ]
persoon_tab <- persoon_tab[RINPERSOON %in% hh_bus$RINPERSOON, ]

persoon_tab_train <- persoon_tab[RINPERSOON %in% train_set$RINPERSOON, ]




assertthat::assert_that(!any(duplicated(sample_rins)))

hh_bus[, merge := paste0(HUISHOUDNR, "_", DATUMAANVANGHH)]

gc()

hh_rins <- unique(hh_bus$merge[hh_bus$RINPERSOON %in% sample_rins])
hh_bus_sample <- hh_bus[hh_bus$merge %in% hh_rins, ]

assertthat::assert_that(all(sample_rins %in% hh_bus_sample$RINPERSOON))

persoon_tab_sample <- persoon_tab[RINPERSOON %in% hh_bus_sample$RINPERSOON, ]
hoogsteopl_tab_sample <- hoogsteopl_tab[RINPERSOON %in% hh_bus_sample$RINPERSOON, ]
# spolis_bus_sample <- spolis_bus[RINPERSOON %in% hh_bus_sample$RINPERSOON, ]


assertthat::assert_that(all(sample_rins %in% hh_bus_sample$RINPERSOON))
assertthat::assert_that(all(sample_rins %in% sample_table$RINPERSOON))

write.csv(sample_table[, .(RINPERSOON, children_post2021)],
          "./bol_generation/data/raw/base_sample.csv")
write.csv(hh_bus_sample, "./bol_generation/data/raw/household_bus.csv")
write.csv(persoon_tab_sample, "./bol_generation/data/raw/persoon_tab.csv")
# write.csv(spolis_bus_sample, "./bol_generation/data/raw/spolis_bus.csv")
write.csv(education_bus_sample, "./bol_generation/data/raw/education_bus.csv")

write.csv(head(hh_bus_sample, 10),
          "./bol_generation/data/raw/household_bus_10.csv")
write.csv(head(persoon_tab_sample, 10),
          "./bol_generation/data/raw/persoon_tab_10.csv")
write.csv(head(spolis_bus_sample, 10),
          "./bol_generation/data/raw/spolis_bus_10.csv")
write.csv(head(education_bus, 10),
          "./bol_generation/data/raw/education_bus_10.csv")

loc <- fread("./data/raw/object_bus_250k.csv")
loc[RINPERSOON == "100015727", ]
