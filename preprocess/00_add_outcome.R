library(data.table)
library(haven)
library(tidyverse)

train_path <- "H:/DATASETS/train.csv"

persoon_tab_sample <- fread("./bol_generation/data/raw/persoon_tab_25k.csv",
                            colClasses = list(character = "RINPERSOON"))

persoon_tab_sample$RINPERSOON

train_set <- fread(train_path)

outcome_dt <- data.table(RINPERSOON = persoon_tab_sample$RINPERSOON)
outcome_dt[, outcome := RINPERSOON %in%
             as.numeric(train_set$RINPERSOON[train_set$children_post2021 == 1])]

sum(outcome_dt$outcome)

write.csv(outcome_dt, "./bol_generation/data/raw/outcome_25k.csv")
