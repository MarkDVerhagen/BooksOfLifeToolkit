library(data.table)

rm(list = ls()
   )
gc()
holdout <- T

education_years <- 1999:2020

read_hoogsteopl <- function(year, educ_path="G:/Onderwijs/HOOGSTEOPLTAB/") {
  files <- list.files(file.path(educ_path, year), pattern=".sav|.SAV")
  sel_file <- files[length(files)]
  print(paste0("Files: ", paste(files)))
  print(paste0("Selecting: ", sel_file))

  temp <- as.data.table(haven::read_sav(file.path(educ_path, year, sel_file)))
  temp[, year := year]
  return(temp)
}

## Temp solution to make education_bus
education_data <- lapply(education_years, read_hoogsteopl)
hoogsteopl_tab <- bind_rows(education_data)
hoogsteopl_tab[, RINPERSOON := as.numeric(RINPERSOON)]

fwrite(hoogsteopl_tab, "./data/raw/hoogsteopl_tab.csv.gz")

hoogsteopl_tab <- fread(
  "./data/raw/hoogsteopl_tab.csv.gz")

names(hoogsteopl_tab)

omit <- c("GEWICHTHOOGSTEOPL",
          "RICHTdetailISCEDF2013HBmetNIRWO",
          "RICHTdetailISCEDF2013HGmetNIRWO",
          "BRONOPLARCHIEFHB",
          "BRONOPLARCHIEFHG",
          "RGEBB")
education_bus <- hoogsteopl_tab[
  , (omit) := NULL]


setnames(education_bus,
         c("OPLNRHB",
           "OPLNRHG",
           "OPLNIVSOI2016AGG4HBMETNIRWO",
           "OPLNIVSOI2021AGG4HBmetNIRWO",
           "OPLNIVSOI2016AGG4HGMETNIRWO",
           "OPLNIVSOI2021AGG4HGmetNIRWO"),
         c("Highest educational credential",
           "Highest educational enrolment",
           "Highest educational credential level (2016)",
           "Highest educational credential level (2021)",
           "Highest educational enrolment level (2016)",
           "Highest educational enrolment level (2021)"))
         
education_bus[, "Highest education credential level" := get("Highest educational credential level (2021)")]
education_bus[is.na(`Highest education credential level`),
              "Highest education credential level" := get("Highest educational credential level (2016)")]

education_bus[, "Highest education enrolment level" := get("Highest educational enrolment level (2021)")]
education_bus[is.na(`Highest education enrolment level`),
              "Highest education enrolment level" := get("Highest educational enrolment level (2016)")]

educ_subset <- 
  education_bus[, .(RINPERSOON, year, `Highest educational credential`,
                  `Highest educational enrolment`, `Highest education credential level`,
                  `Highest education enrolment level`
                  )]

educ_subset <- educ_subset[order(RINPERSOON, year), ]

rins <- length(unique(educ_subset$RINPERSOON))

columns_for_distinct <- setdiff(names(educ_subset), "year")

educ_subset_distinct <- unique(educ_subset, by = columns_for_distinct)

rins_distinct <- length(unique(educ_subset_distinct$RINPERSOON))

assertthat::assert_that(rins_distinct == rins)

## Add coding
opl_coding <- readxl::read_xlsx(
  "K:/Utilities/Code_Listings/SSBreferentiebestanden/Opleidingnrrefv32waardenvariabelen.xlsx",
  skip = 1) %>%
  as.data.table()

opl_names <- function(educ, opl_coding,
                      var = "Highest educational credential") {
  hbopl <- educ[[var]]
  assertthat::assert_that(all(hbopl[!is.na(hbopl)] %in% opl_coding$Value))
  
  merge_hb <- opl_coding[, .(Value, Label)]
  merge_hb <- merge_hb[Value %in% hbopl, ]
  merge_hb <- merge_hb[!duplicated(merge_hb$Value), ]
  merge_hb[, Value := as.numeric(Value)]
  
  setnames(merge_hb, "Value", var)
  educ <- educ %>% left_join(merge_hb)
  educ[[var]] <- ifelse(!is.na(educ$Label),
                        educ$Label, educ[[var]])
  educ$Label <- NULL
  return(educ)
}

educ_subset_distinct_hb <- opl_names(educ_subset_distinct, opl_coding,
          var = "Highest educational credential")
educ_subset_distinct_hb_hb <- opl_names(educ_subset_distinct_hb, opl_coding,
                                        var = "Highest educational enrolment")
educ_subset_distinct_hb_hb[
  educ_subset_distinct_hb_hb$`Highest educational credential` !=
    educ_subset_distinct_hb_hb$`Highest educational enrolment`,
]


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
  
  sample_table <- educ_subset_distinct_hb_hb[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/education_bus{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
  if (holdout) {
    break
  }
}
