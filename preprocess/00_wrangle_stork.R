library(data.table)
library(dplyr)

candidate_files <- list.files("H:/pmt/stork_oracle_predictions_for_cruijff/", pattern="predictions_for.*train", recursive=TRUE)
base_sample <- fread("./data/raw/base_sample.csv")
holdout_sample <- fread("./data/raw/base_sample_holdout.csv")

versions <- c(2)

for (version in versions) {
  version_str <- paste0("v", version)
  train_file <- candidate_files[grepl(paste0("for_train_set_", version_str), candidate_files)]
  holdout_file <- candidate_files[grepl(paste0("for_final_set_", version_str), candidate_files)]
  stork_preds_train <- fread(
    file.path("H:/pmt/stork_oracle_predictions_for_cruijff/", train_file))
  stork_preds_holdout <- fread(
    file.path("H:/pmt/stork_oracle_predictions_for_cruijff/", holdout_file))

  stork_preds <- bind_rows(stork_preds_train,
                           stork_preds_holdout)
  
  assertthat::assert_that(all(
    unlist(lapply(stork_preds$prediction, is.numeric))))
  
  set.seed(1704)
  setnames(stork_preds, "prediction", "p")
  stork_preds$p <- round(stork_preds$p*100)
  
  full_sample <- bind_rows(base_sample, holdout_sample)
  
  stork_preds_full <- full_sample %>% left_join(stork_preds)
  stork_preds_full$children_post2021 <- NULL
  
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
    
    sample_table <- stork_preds_full[RINPERSOON %in% base_sample$RINPERSOON, ]
    print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
    
    out_file <- glue("./data/raw/stork{version}_tab{k}.csv")
    print(glue("Now writing: {out_file}"))
    fwrite(sample_table, out_file)
    if (holdout) {
      break
    }
  }
}