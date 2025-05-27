library(data.table)
library(haven)
library(tidyverse)
library(glue)

sample_n_list <- c(250000, 500000, 1000000, 0)

train_path <- "H:/DATASETS/train.csv"

train_set <- fread(train_path)

for (n in sample_n_list) {
  set.seed(1704)
  if (n == 0) {
    sample_rins <- unique(train_set$RINPERSOON)
    k <- ""
  } else {
    sample_rins <- sample(train_set$RINPERSOON, n)  
    k <- paste0("_", round(n / 1000), "k")
  }
  
  sample_table <- train_set[RINPERSOON %in% sample_rins, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/base_sample{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table[, .(RINPERSOON, children_post2021)],
            out_file)
}

## Generate holdout
holdout <- fread("H:/DATASETS/holdout_final_leaderboard.csv")

holdout[, children_post2021 := NA]

sample_table <- holdout[, .(RINPERSOON, children_post2021)]
k <- "_holdout"

out_file <- glue("./data/raw/base_sample{k}.csv")
print(glue("Now writing: {out_file}"))
fwrite(sample_table[, .(RINPERSOON, children_post2021)],
       out_file)
