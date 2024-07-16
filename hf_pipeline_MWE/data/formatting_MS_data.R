# I got the fine tuning recipe to work on July 3, but it was taking a lot of time, so I 
# want to train on a subset of these data 

library(tidyverse)
library(random)


subset_size <- 100

data <- read_csv("fake_data_for_tuning_3cols.csv")

data_subset <- data %>%
    sample_n(subset_size)

write_csv(data_subset, "fake_data_for_tuning_3cols_subset.csv")