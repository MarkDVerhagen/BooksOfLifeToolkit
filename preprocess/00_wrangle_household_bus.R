library(data.table)
library(glue)

household_path <- "G:/Bevolking/GBAHUISHOUDENSBUS/geconverteerde data/GBAHUISHOUDENS2020BUSV1.csv"
hh_bus <- fread(household_path)
hh_bus[, merge := paste0(HUISHOUDNR, "_", DATUMAANVANGHH)]

gc()

make_sets <- function(data, sample_list=c(250000, 500000, 1000000, 0),
                      holdout=FALSE, hh_bus=FALSE, name="household_bus") {
  
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
    if (hh_bus) {
      hh_rins <- unique(data$merge[data$RINPERSOON %in% base_sample$RINPERSOON])
      sample <- data[data$merge %in% hh_rins, ]
    } else {
      sample <- data[RINPERSOON %in% base_sample$RINPERSOON, ]
    }
    
    
    print(glue("Writing a dataframe of size {dim(sample)[1]} rows"))
    
    out_file <- glue("./data/raw/{name}{k}.csv")
    print(glue("Now writing: {out_file}"))
    fwrite(sample, out_file)
    if (holdout) {
      break
    }
  }
}


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
  
  hh_rins <- unique(hh_bus$merge[hh_bus$RINPERSOON %in% base_sample$RINPERSOON])
  hh_bus_sample <- hh_bus[hh_bus$merge %in% hh_rins, ]
  
  print(glue("Writing a dataframe of size {dim(hh_bus_sample)[1]} rows"))
  
  out_file <- glue("./data/raw/household_bus{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(hh_bus_sample, out_file)
  if (holdout) {
    break
  }
}
