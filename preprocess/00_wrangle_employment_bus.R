library(data.table)
library(dplyr)

rm(list = ls())
gc()
holdout <- T
# 
# base_set <- fread("./data/raw/base_sample.csv")
# holdout_set <- fread("./data/raw/base_sample_holdout.csv")
# 
# base_set_rins <- c(base_set$RINPERSOON, holdout_set$RINPERSOON)
# 
# employment_years <- 2010:2020
# 
# read_spolis <- function(year, base_set_rins,
#                         spolis_path="G:/Spolis/SPOLISBUS/") {
#   files <- list.files(file.path(spolis_path, year, "geconverteerde data"),
#                       pattern = ".csv")
#   files_version <- gsub(".*V", "", files)
#   files_version <- as.numeric(gsub(".csv", "", files_version))
#   max_v <- max(files_version)
#   sel_file <- files[grepl(paste0("V", max_v), files)]
# 
#   print(paste0("Files: ", paste(files)))
#   print(paste0("Selecting: ", sel_file))
# 
#   temp <- fread(file.path(spolis_path, year,
#                           "geconverteerde data", sel_file))
#   temp <- temp[
#     , .(RINPERSOON, IKVID, SDATUMAANVANGIKO, SDATUMEINDEIKO,
#         SBASISUREN, SLNLBPH, SLNOWRK,
#         SVOLTIJDDAGEN, SCDAARD, SCDINCINKVERM,
#         SCONTRACTSOORT, SDATUMAANVANGIKVORG,
#         SPOLISDIENSTVERBAND, SSECT, SSOORTBAAN)]
#   temp <- temp[RINPERSOON %in% base_set_rins, ]
#   temp[, year := year]
#   print(paste0("Dimensions of file: ", dim(temp)))
#   return(temp)
# }
# 
# spolis_files <- lapply(employment_years, read_spolis,
#                        base_set_rins = base_set_rins)
# 
# gc()
# 
# spolis_bus <- rbindlist(spolis_files)
# 
# assertthat::assert_that(
#   all(unique(spolis_bus$RINPERSOON) %in% c(base_set$RINPERSOON,
#                                            holdout_set$RINPERSOON)))
# 
# fwrite(spolis_bus, "./data/raw/spolis_bus_v2.csv.gz")
# rm(spolis_files)
# gc()

spolis_bus <- fread("./data/raw/spolis_bus_v2.csv.gz")

spolis_bus[, start_date := as.Date(
  as.character(SDATUMAANVANGIKO), format="%Y%m%d")]
spolis_bus[, end_date := as.Date(
  as.character(SDATUMEINDEIKO), format="%Y%m%d")]

job_cols <- c("SSOORTBAAN", "SSECT", "SPOLISDIENSTVERBAND",
              "SCONTRACTSOORT", "SCDINCINKVERM", "SCDAARD",
              "IKVID")

setdiff(names(spolis_bus), job_cols)

spolis_bus[, SBASISUREN_num := as.numeric(gsub("\\,.*", "", SBASISUREN))]

spolis_bus[is.na(SBASISUREN_num), SBASISUREN_num := 1]

spolis_codes <- readxl::read_xlsx("./data/raw/spolis_codes.xlsx",
                                  sheet = "waarden") %>%
  as.data.table()

for (col in job_cols[1:6]) {
  col_dict <- spolis_codes[Variable == col, ]
  col_dict <- col_dict[, .(Value, Label)]
  
  old_vals <- unique(spolis_bus[[col]])
  print(old_vals)
  
  setnames(col_dict, "Value", col)
  spolis_bus[, (col) := as.character(get(col))]
  spolis_bus <- spolis_bus %>%
    left_join(col_dict)
  spolis_bus[[col]] <- NULL
  setnames(spolis_bus, "Label", col)
  
  
  new_vals <- unique(spolis_bus[[col]])
  print(new_vals)
  print(paste0("Mean NA: ", mean(is.na(spolis_bus[[col]]))))
}

setorder(spolis_bus, RINPERSOON, IKVID, start_date)
spolis_bus[, job_enumerator := 0L]
spolis_bus[, previous_end_date := shift(end_date, type = "lag"),
                by = c("RINPERSOON", job_cols)]
spolis_bus[
  , job_enumerator := cumsum(
    ifelse(is.na(previous_end_date), 0L,
           (as.numeric(start_date - previous_end_date) > 2))),
                by = c("RINPERSOON", job_cols)]

spolis_bus[
  , spell_enumerator := .GRP, by = c("RINPERSOON", job_cols)
]

spolis_bus[
  , comp_enumerator := spell_enumerator + job_enumerator
]

jobs <- spolis_bus[
  , .(
    start_date = min(start_date),
    end_date = max(end_date),
    mean_salary = mean(SLNLBPH),
    sd_salary = sd(SLNLBPH),
    mean_monthly_hours = mean(SBASISUREN_num),
    sd_monthly_hours = sd(SBASISUREN_num)
    ), by = c(job_cols, "RINPERSOON", "comp_enumerator")]

jobs$comp_enumerator <- NULL

jobs$mean_salary <- round(jobs$mean_salary)
jobs$sd_salary <- round(jobs$sd_salary)
jobs$mean_monthly_hours <- round(jobs$mean_monthly_hours)
jobs$sd_monthly_hours <- round(jobs$sd_monthly_hours)

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
  
  sample_table <- jobs[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/employment_bus{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
  if (holdout) {
    break
  }
}


