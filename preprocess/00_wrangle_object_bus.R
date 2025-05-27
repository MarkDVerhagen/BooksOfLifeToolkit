
rm(list = ls()
)
gc()
library(data.table)
library(dplyr)
library(glue)

holdout <- T

object_bus <- haven::read_sav(
  "G:/Bevolking/GBAADRESOBJECTBUS/GBAADRESOBJECT2020BUSV1.sav")

object_bus <- object_bus %>%
  as.data.table()

object_bus[, RINPERSOON := as.numeric(RINPERSOON)]

## Make sure we don't include 2021 data
object_bus <- object_bus[!substr(GBADATUMAANVANGADRESHOUDING, 1, 4) == "2021",]
object_bus <- object_bus[substr(GBADATUMEINDEADRESHOUDING, 1, 4) == "2021",
           GBADATUMEINDEADRESHOUDING := "20501231"]

assertthat::assert_that(
  !any(unique(substr(object_bus$GBADATUMEINDEADRESHOUDING, 1, 4)) == "2021"))
assertthat::assert_that(
  !any(unique(substr(object_bus$GBADATUMSTARTADRESHOUDING, 1, 4)) == "2021"))

vslgwb <- fread("G:/BouwenWonen/VSLGWBTAB/geconverteerde data/VSLGWB2022TAB03V2.csv",
                encoding="Latin-1")

vslgwb_codes <- haven::read_sav("G:/BouwenWonen/VSLGWBTAB/VSLGWB2023TAB03V1.sav",
                                col_select = c("RINOBJECTNUMMER", "gem2020",
                                               "wc2020", "bc2020"))
vslgwb_codes <- as.data.table(vslgwb_codes)

vslgwb_type <- haven::read_sav(
  "G:/BouwenWonen/VBOWONINGTYPETAB/VBOWONINGTYPE2020TABV2.sav")
vslgwb_type <- as.data.table(vslgwb_type)
vslgwb_rel <- vslgwb[, .(SOORTOBJECTNUMMER, RINOBJECTNUMMER,
                         gem2020, wc2020, bc2020)]

vslgwb_rel <- distinct(vslgwb_rel)
vslgwb_rel <- vslgwb_rel[!duplicated(vslgwb_rel$RINOBJECTNUMMER), ]
vslgwb_codes <- vslgwb_codes[RINOBJECTNUMMER %in%
                               vslgwb_rel$RINOBJECTNUMMER, ]
vslgwb_type <- vslgwb_type[RINOBJECTNUMMER %in% vslgwb_rel$RINOBJECTNUMMER, ]

base_sample <- fread("./data/raw/base_sample.csv")
holdout_sample <- fread("./data/raw/base_sample_holdout.csv")

object_bus_rel <- object_bus[(RINPERSOON %in% base_sample$RINPERSOON) |
                               (RINPERSOON %in% holdout_sample$RINPERSOON), ]
setkey(object_bus_rel, "RINOBJECTNUMMER")
setkey(vslgwb_rel, "RINOBJECTNUMMER")
setkey(vslgwb_codes, "RINOBJECTNUMMER")
setkey(vslgwb_type, "RINOBJECTNUMMER")

assertthat::assert_that(all(
  vslgwb_type$RINOBJECTNUMMER %in% vslgwb_rel$RINOBJECTNUMMER))
assertthat::assert_that(
  all(base_sample$RINPERSOON %in% object_bus_rel$RINPERSOON))
assertthat::assert_that(
  mean(object_bus_rel$RINOBJECTNUMMER %in% vslgwb_rel$RINOBJECTNUMMER) > 0.99)
assertthat::assert_that(
  all(vslgwb_rel$RINOBJECTNUMMER %in% vslgwb_codes$RINOBJECTNUMMER))

vslgwb_rel$SOORTOBJECTNUMMER <- NULL

vslgwb_rel_codes <- vslgwb_codes[vslgwb_rel]
vslgwb_rel_codes_types <- vslgwb_type[vslgwb_rel_codes]
location_bus <- vslgwb_rel_codes_types[object_bus_rel]

rm(base_sample, holdout_sample, object_bus, object_bus_rel, vslgwb,
   vslgwb_codes)
gc()

location_bus$i.gem2020 <- NULL
location_bus$i.wc2020 <- NULL
location_bus[, location_desc := as.character(location_bus$i.bc2020)]
location_bus[, location_desc := gsub("^Gemeente", "Municipality:", location_desc)]
location_bus[, location_desc := gsub("; Wijk", "; District", location_desc)]
location_bus[, location_desc := gsub("; Buurt", "; Neighborhood", location_desc)]

location_bus[, start_date := as.Date(GBADATUMAANVANGADRESHOUDING,
                                     format="%Y%m%d")]
location_bus[, end_date := as.Date(GBADATUMEINDEADRESHOUDING,
                                     format="%Y%m%d")]
location_bus$RINPERSOONS <- NULL
location_bus$gem2020 <- NULL
location_bus$gem2020 <- NULL
location_bus$i.SOORTOBJECTNUMMER <- NULL
location_bus[VBOWoningtype == "01", VBOWoningtype := "Vrijstaande woning"]
location_bus[VBOWoningtype == "02", VBOWoningtype := "Twee-onder-een-kapwoning"]
location_bus[VBOWoningtype == "03", VBOWoningtype := "Hoekwoning"]
location_bus[VBOWoningtype == "04", VBOWoningtype := "Tussenwoning"]
location_bus[VBOWoningtype == "05", VBOWoningtype := "Meergezinswoning"]
location_bus[VBOWoningtype == "99", VBOWoningtype := "Onbekend"]
location_bus[is.na(VBOWoningtype), VBOWoningtype := "Geen woningindicatie"]

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
  
  sample_table <- location_bus[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/object_bus{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
  if (holdout) {
    break
  }
}
