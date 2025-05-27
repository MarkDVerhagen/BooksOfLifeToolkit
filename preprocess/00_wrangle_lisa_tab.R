library(data.table)
library(glue)
library(tidyverse)

rm(list = ls()
)
gc()
holdout <- T

train_path <- "H:/DATASETS/train.csv"

lisa_tab <- fread(train_path)

rel_lisa_tab <- lisa_tab[, .(RINPERSOON,
                             children_pre2021,
                             birthday_youngest,
                             marriages_total, ## partners
                             partnerships_total,
                             GBABURGERLIJKESTAATNW,
                             AANVANGVERBINTENIS,
                             GBAGEBOORTEJAARPARTNER,
                             GBAGEBOORTEMAANDPARTNER,
                             GBAGEBOORTELANDPARTNER,
                             GBAGESLACHTPARTNER,
                             OPLNIVSOI2021AGG4HBmetNIRWO_partner,
                             OPLNIVSOI2021AGG4HGmetNIRWO_partner,
                             SECM_partner,
                             INHEHALGR, ## Wealth
                             INHPOPIIV,
                             INHSAMAOW,
                             INHSAMHH,
                             INHUAF,
                             INHUAFL,
                             INHUAFTYP,
                             VEHP100WELVAART,
                             VEHW1000VERH,
                             VEHP100HVERM,
                             VEHW1100BEZH,
                             VEHW1110FINH,
                             VEHW1120ONRH,
                             VEHW1130ONDH,
                             VEHW1140ABEH,
                             VEHW1150OVEH,
                             VEHW1200STOH,
                             VEHW1210SHYH,
                             VEHW1220SSTH,
                             VEHW1230SOVH,
                             VEHWVEREXEWH,
                             INPBELI, ## Income
                             INPEMEZ,
                             INPEMFO,
                             INPP100PBRUT,
                             INPP100PPERS,
                             INPPERSPRIM,
                             INPPINK,
                             INPPOSHHK,
                             INHAHL,
                             INHAHLMI,
                             INHARMEUR,
                             INHARMEURL,
                             INHBBIHJ,
                             INHBRUTINKH,
                             VEHW1000VERH, ## location
                             VZAFSTANDKDV,
                             VZAANTKDV01KM,
                             VZAANTKDV03KM,
                             VZAANTKDV05KM,
                             VZAFSTANDBSO,
                             VZAANTBSO01KM,
                             VZAANTBSO03KM,
                             VZAANTBSO05KM
                             )]


## ENCODE
country_codes <- fread("./data/raw/country_codes.csv")
country_codes$Code <- str_pad(country_codes$Code, 4, "left", "0")

coded_list <- setNames(country_codes$Land,
                       country_codes$Code)

rel_lisa_tab[, GBAGEBOORTELANDPARTNER :=
               coded_list[as.character(GBAGEBOORTELANDPARTNER)]]

coded_list <- setNames(c("Male", "Female"), c("1", "2"))

civil_codes <- fread("./data/raw/civil_codes.csv")

coded_list <- setNames(civil_codes$Code,
                       civil_codes$GBABURGERLIJKESTAATNW)
rel_lisa_tab[, GBABURGERLIJKESTAATNW :=
               coded_list[as.character(GBABURGERLIJKESTAATNW)]]


coded_list <- setNames(
  c(
    "Werknemer",
    "Directeur-grootaandeelhouder",
    "Zelfstandig ondernemer",
    "Overige zelfstandige",
    "Ontvanger werkloosheidsuitkering",
    "Ontvanger bijstandsuitkering",
    "Ontvanger uitkering sociale voorz.overig",
    "Ontvanger uitkering ziekte/AO",
    "Ontvanger pensioenuitkering",
    "Nog niet schoolg./schol./stud. met ink.",
    "Nog niet schoolg./schol./stud. geen ink.",
    "Overig zonder inkomen",
    "Meewerkend gezinslid"
  ),
  c("11", "12", "13", "14", "21",
    "22", "23", "24", "25", "26",
    "31", "32", "15")
)

rel_lisa_tab[, SECM_partner :=
               coded_list[as.character(SECM_partner)]]

coded_list <- setNames(
  c("No personal income",
    "With personal income",
    "No income observed"),
  c("0", "1", "9")
)

rel_lisa_tab[, INPPINK :=
               coded_list[as.character(INPPINK)]]

inpposhhk_codes <- fread("./data/raw/inpposhhk_codes.csv")

coded_list <- setNames(
  inpposhhk_codes$Code,
  inpposhhk_codes$INPPOSHHK
)

rel_lisa_tab[, INPPOSHHK :=
               coded_list[as.character(INPPOSHHK)]]

## INPEMEZ
coded_list <- setNames(
  c("Not independent",
    "Independent",
    "Not target population",
    "Not observed"),
  c(0, 1, 8, 9)
)

rel_lisa_tab[, INPEMEZ :=
               coded_list[as.character(INPEMEZ)]]

## INPEMFO
rel_lisa_tab[, INPEMFO :=
               coded_list[as.character(INPEMFO)]]

## INHEHALGR
coded_list <- setNames(
  c("Own house", "Rental w/o aid",
    "Rental w aid", "Institutional",
    "Unknown"),
  c(1,2,3,8,9)
)

rel_lisa_tab[, INHEHALGR :=
               coded_list[as.character(INHEHALGR)]]

# INHPOPIIV
coded_list <- setNames(
  c(
    "Particulier huishouden met waarneming inkomen; geen studentenhuishouden",
    "Particulier studentenhuishouden met waarneming inkomen",
    "Institutioneel huishouden, eenheid met waarneming inkomen",
    "Particulier huishouden zonder waarneming inkomen",
    "Institutioneel huishouden, eenheid zonder waarneming inkomen",
    "Particulier, maar niet behorend tot huishoudenspopulatie (niet ingedeelde personen)"
  ),
  c("1",
    "2",
    "3",
    "7",
    "8",
    "9")
)

rel_lisa_tab[, INHPOPIIV :=
               coded_list[as.character(INHPOPIIV)]]

# INHUAFTYP
coded_list <- setNames(
    c(
      "Geen uitkering",
      "Werkloosheidsuitkering",
      "Arbeidsongeschiktheidsuitkering",
      "Bijstandsuitkering",
      "Uitkering overige sociale voorziening",
      "Institutioneel huishouden",
      "Particulier huishouden met onbekend inkomen"
    ),
    c(
      "0", "1", "2",
      "3", "4", "8", "9"
    ))

rel_lisa_tab[, INHUAFTYP :=
               coded_list[as.character(INHUAFTYP)]]

# INHBBIHJ

coded_list <- setNames(
  c(
    "Loon",
    "Loon directeur-grootaandeelhouder",
    "Winst zelfstandig ondernemer",
    "Inkomen overige zelfstandige",
    "Werkloosheidsuitkering",
    "Bijstandsuitkering",
    "Uitkering sociale voorziening overig",
    "Uitkering ziekte/arbeidsongeschiktheid",
    "Pensioenuitkering",
    "Studiefinanciering",
    "Inkomen uit vermogen",
    "Huishoudensinkomen onbekend"
  ),
  c(
    "11","12","13","14","21","22","23","24","25","26","30","99"
  )
)

rel_lisa_tab[, INHBBIHJ :=
               coded_list[as.character(INHBBIHJ)]]

for (n in c(250000, 500000, 1000000, 0)) {
  if (n == 0) {
    k <- ""
  } else {
    k <- paste0("_", round(n / 1000), "k")
  }
  
  in_file <- glue("./data/raw/base_sample{k}.csv")
  base_sample <- fread(in_file)
  
  sample_table <- rel_lisa_tab[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/lisa_tab{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
}

loc_lisa_tab <- rel_lisa_tab[, .(
  RINPERSOON,
  VZAFSTANDKDV,
  VZAANTKDV01KM,
  VZAANTKDV03KM,
  VZAANTKDV05KM,
  VZAFSTANDBSO,
  VZAANTBSO01KM,
  VZAANTBSO03KM,
  VZAANTBSO05KM
)]

for (n in c(250000, 500000, 1000000, 0)) {
  if (n == 0) {
    k <- ""
  } else {
    k <- paste0("_", round(n / 1000), "k")
  }
  
  in_file <- glue("./data/raw/base_sample{k}.csv")
  base_sample <- fread(in_file)
  
  sample_table <- loc_lisa_tab[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/loc_lisa_tab{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
}

wealth_lisa_tab <- rel_lisa_tab[, .(
  RINPERSOON,
  INHEHALGR,
  INHPOPIIV,
  INHSAMAOW,
  INHSAMHH,
  INHUAF,
  INHUAFL,
  INHUAFTYP,
  VEHP100WELVAART,
  VEHW1000VERH,
  VEHW1100BEZH,
  VEHW1110FINH,
  VEHW1120ONRH,
  VEHW1130ONDH,
  VEHW1140ABEH,
  VEHW1150OVEH,
  VEHW1200STOH,
  VEHW1210SHYH,
  VEHW1220SSTH,
  VEHW1230SOVH,
  VEHWVEREXEWH
)]

for (n in c(250000, 500000, 1000000, 0)) {
  if (n == 0) {
    k <- ""
  } else {
    k <- paste0("_", round(n / 1000), "k")
  }
  
  in_file <- glue("./data/raw/base_sample{k}.csv")
  base_sample <- fread(in_file)
  
  sample_table <- wealth_lisa_tab[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/wealth_lisa_tab{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
}

inc_lisa_tab <- rel_lisa_tab[, .(
  RINPERSOON,
  INPBELI, ## Income
  INPEMEZ,
  INPEMFO,
  INPP100PBRUT,
  INPP100PPERS,
  INPPERSPRIM,
  INPPINK,
  INPPOSHHK,
  INHAHL,
  INHAHLMI,
  INHARMEUR,
  INHARMEURL,
  INHBBIHJ,
  INHBRUTINKH
)]

for (n in c(250000, 500000, 1000000, 0)) {
  if (n == 0) {
    k <- ""
  } else {
    k <- paste0("_", round(n / 1000), "k")
  }
  
  in_file <- glue("./data/raw/base_sample{k}.csv")
  base_sample <- fread(in_file)
  
  sample_table <- inc_lisa_tab[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/inc_lisa_tab{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
}

par_lisa_tab <- rel_lisa_tab[, .(
  RINPERSOON,
  marriages_total, ## partners
  partnerships_total,
  GBABURGERLIJKESTAATNW,
  AANVANGVERBINTENIS,
  GBAGEBOORTEJAARPARTNER,
  GBAGEBOORTEMAANDPARTNER,
  GBAGEBOORTELANDPARTNER,
  GBAGESLACHTPARTNER,
  OPLNIVSOI2021AGG4HBmetNIRWO_partner,
  OPLNIVSOI2021AGG4HGmetNIRWO_partner,
  SECM_partner
)]

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
  
  sample_table <- par_lisa_tab[RINPERSOON %in% base_sample$RINPERSOON, ]
  print(glue("Writing a dataframe of size {dim(sample_table)[1]} rows"))
  
  out_file <- glue("./data/raw/par_lisa_tab{k}.csv")
  print(glue("Now writing: {out_file}"))
  fwrite(sample_table, out_file)
  if (holdout) {
    break
  }
}
