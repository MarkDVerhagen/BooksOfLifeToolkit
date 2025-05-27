library(data.table)
library(dplyr)

sample <- fread("./data/raw/base_sample_250k.csv")

persoon <- fread("./data/raw/persoon_tab_250k.csv")

df <- sample %>%
  left_join(persoon[, .(RINPERSOON, GBAGEBOORTEJAAR, GBAGESLACHT)])

frame <- df %>%
  group_by(
    GBAGESLACHT,
    GBAGEBOORTEJAAR
  ) %>%
  summarise(p_hat = mean(children_post2021))


df_inc_p <- df %>% left_join(frame)

df_inc_p_sample <- df_inc_p

MLmetrics::LogLoss(df_inc_p$p_hat, df_inc_p$children_post2021)

train <- fread("H:/DATASETS/train.csv")

seed <- fread(
  "H:/pmt/eval/train_and_eval_samples/pmt_train_and_evaluation_samples_seed_1a.csv")
seed_ossc <- fread("H:/pmt/cruijff_runs/pmt_train_and_evaluation_samples_seed_1.csv")
