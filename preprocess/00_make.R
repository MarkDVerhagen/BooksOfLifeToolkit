
## Make base sets with RINPERSOON and outcome only
source("00_wrangle_sets.R")

## Make persoon_tab
source("00_wrangle_persoon_tab.R")
rm(list = ls())
gc()

## Make householdbus
source("00_wrangle_household_bus.R")
rm(list = ls())
gc()

## Make education_bus
source("00_wrangle_education_bus.R")
rm(list = ls())
gc()

## Make employment_bus
source("00_wrangle_employment_bus.R")
rm(list = ls())
gc()

## Make object_bus
source("00_wrangle_object_bus.R")
rm(list = ls())
gc()

## Make lisa_tab
source("00_wrangle_lisa_tab.R")
rm(list = ls())
gc()
