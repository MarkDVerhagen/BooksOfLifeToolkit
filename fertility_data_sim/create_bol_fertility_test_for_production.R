rm(list=ls())
library(tidyverse)
library(rlang)
library(conflicted)
library(assertthat)
set.seed(08544)

# set parameters
n_chad <- 5000
n_netherlands <- 5000
n_south_korea <- 5000

age <- 18:45
country <- c("Chad", "Netherlands", "South Korea")
desire <- c("wants a baby", "doesn't want a baby")

# tibble of all possible parameter combinations
param_combos <- expand_grid(age = age, country = country, desire = desire)

# create people
prop_desire_chad <- 0.3
chad_desire <- c(rep("wants a baby", round(n_chad * prop_desire_chad)), 
                     rep("doesn't want a baby", n_chad - round(n_chad * prop_desire_chad)))
ages_chad <- c(sample(18:45, n_chad, replace = TRUE))

prop_desire_netherlands <- 0.3
netherlands_desire <- c(rep("wants a baby", round(n_netherlands * prop_desire_netherlands)), 
                     rep("doesn't want a baby", n_netherlands - round(n_netherlands * prop_desire_netherlands)))
ages_netherlands <- ages_chad # assume same age distribution as Chad

prop_desire_south_korea <- 0.3
south_korea_desire <- c(rep("wants a baby", round(n_south_korea * prop_desire_south_korea)), 
  rep("doesn't want a baby", n_south_korea - round(n_south_korea * prop_desire_south_korea)))
ages_south_korea <- ages_chad # assume same age distribution as Chad

people <- tibble(
    RINPERSOON = 1:(n_chad + n_netherlands + n_south_korea),
    country = c(rep("Chad", n_chad), rep("Netherlands", n_netherlands), rep("South Korea", n_south_korea)),
    desire = c(chad_desire, netherlands_desire, south_korea_desire),
    age = c(ages_chad, ages_netherlands, ages_south_korea)
)

convert_demographics_to_probability <- function(age, country, desire) {
  # fundtion to convert demographics to probability of having a kid

  # write tests of input
  assert_that(country %in% c("Chad", "Netherlands", "South Korea"))
  assert_that(desire %in% c("wants a baby", "doesn't want a baby"))
  assert_that(age >= 18 & age <= 45)

  # set by trial and error https://www.desmos.com/calculator
  a <- -0.006
  b <- 0.1
  c <- -1
  country_offset <- case_when(
    country == "Netherlands" ~ -0.8,
    country == "Chad" ~ 0.1,
    country == "South Korea" ~ -1.5
  )
  desire_hash <- case_when(
    desire == "wants a baby" ~ 1.5,
    desire == "doesn't want a baby" ~ -1
  )
  
  # log odds of having a kid
  log_odds_kid <- a * (age - 18)^2 + b * (age - 18) + c + country_offset + desire_hash
  
  # Convert log odds to probability
  p_kid <- 1 / (1 + exp(-log_odds_kid))
  
  assert_that(p_kid >= 0 & p_kid <= 1)
  return(p_kid)
}

# apply function to all rows of people
people <- people %>%
  mutate(true_probability = pmap_dbl(list(age, country, desire), convert_demographics_to_probability))

# simulate having a kid
people <- people %>% 
  mutate(labels = rbinom(n(), 1, true_probability))

# append hashed version of each column
people <- people %>%
  mutate(
    RINPERSOON_hash = hash(RINPERSOON),
    age_hash = hash(age),
    country_hash = hash(country),
    desire_hash = hash(desire)
  )

# add text
people <- people %>%
  mutate(text = str_glue("RINPERSOON is {RINPERSOON}, country is {country}, age is {age}, desire is {desire}")) %>%
  mutate(text_hashed = str_glue("RINPERSOON is {RINPERSOON_hash}, country is {country_hash}, age is {age_hash}, desire is {desire_hash}")) 

# write people to csv file
people %>%
  select(RINPERSOON, text, labels, true_probability) %>%
  write_csv("bol_fertility_test.csv")

# write people to HF dataset
# Import the datasets Python module
datasets <- reticulate::import("datasets")

# Convert the dataframe to a Python dictionary
py_dict <- reticulate::r_to_py(as.data.frame(df))

# Create a Hugging Face Dataset
dataset <- datasets$Dataset$from_dict(py_dict)

# Save the dataset
dataset$save_to_disk("your_dataset_name")