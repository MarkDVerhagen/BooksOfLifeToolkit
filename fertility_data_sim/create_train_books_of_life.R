rm(list=ls(()))
library(tidyverse)
library(tidymodels)
library(rlang)
library(conflicted)
set.seed(08544)

age <- 18:45
country <- c("Chad", "Netherlands", "South Korea")
desire <- c("wants a baby", "doesn't want a baby")

# tibble of all possible parameter combinations
param_combos <- expand_grid(age = age, country = country, desire = desire)

# this code is not very efficient in R but I'm trying to write in a way that I can swtich to Python eventually
for (row in 1:nrow(param_combos)) {
  # age
  age <- param_combos[row, "age"]

  # country
  country <- param_combos[row, "country"]

  # desire
  desire <- param_combos[row, "desire"]
  
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
  
  # Append to param_combos
  param_combos[row, c("log_odds_kid", "p_kid")] <- c(log_odds_kid, p_kid)
}

# ggplot age vs p_kid facet by country and desire
g <- param_combos %>%
  select(age, p_kid, country, desire) %>%
  ggplot(aes(age, p_kid)) +
  geom_line() +
  facet_grid(country ~ desire) +
  labs(title = "",
       x = "Age",
       y = "Probability of having a kid", 
       caption = paste(Sys.time()))

ggsave(filename = "figures/fer_sim_dgp.png", plot = g)

# write param_combos to csv
write_csv(param_combos, "data/fer_sim_dpg_params.csv")

# set parameters
n_chad <- 5000
n_netherlands <- 5000
n_south_korea <- 5000

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
  person_id = 1:(n_chad + n_netherlands + n_south_korea),
  country = c(rep("Chad", n_chad), rep("Netherlands", n_netherlands), rep("South Korea", n_south_korea)),
  desire = c(chad_desire, netherlands_desire, south_korea_desire),
  age = c(ages_chad, ages_netherlands, ages_south_korea)
)

# join probabilities from param_combos
people <- left_join(people, param_combos, 
                    by = c("country", "age", "desire"))

# simulate having a kid
people <- people %>%
  mutate(
    kid = rbinom(n(), 1, p_kid)
  )

# append hashed version of each column
people <- people %>%
  mutate(
    person_id_hash = hash(person_id),
    age_hash = hash(age),
    country_hash = hash(country),
    desire_hash = hash(desire)
  )




# write instruction file

#header <- "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request." 
#instruction <- "You are a smart, helpful AI assistant."
#
#people <- people %>%
#  mutate(instruction = instruction) %>%
#  mutate(input = str_glue("person_id is {person_id}, country is {country}, age is {age}, desire is {desire}")) %>%
#  mutate(input_hash = str_glue("person_id is {person_id}, country is {country_hash}, age is {age_hash}, desire is {desire_hash}")) %>%
#  mutate(response = str_glue("kid: {kid}")) %>%
#  mutate(text = str_glue("{header}\n\n ### Instruction:\n{instruction}\n\n ### Input:\n{input}\n\n ### Response:\n{response}")) %>%
#  mutate(text_hash = str_glue("{header}\n\n ### Instruction:\n{instruction}\n\n ### Input:\n{input_hash}\n\n ### Response:\n{response}"))

people <- people %>%
  mutate(prompt = str_glue("person_id is {person_id}, country is {country}, age is {age}, desire is {desire}")) %>%
  mutate(prompt_hash = str_glue("person_id is {person_id}, country is {country_hash}, age is {age_hash}, desire is {desire_hash}")) %>%
  mutate(completion = str_glue("child: {kid}")) %>%
  mutate(sample = str_glue('{{"prompt": "{prompt}", "completion": "{completion}"}}')) %>%
  mutate(sample_hashed = str_glue('{{"prompt": "{prompt_hash}", "completion": "{completion}"}}'))
 
# Create the split
split <- initial_split(people, prop = 0.9)

# Extract training and testing sets
train_data <- training(split)
n_train <- nrow(train_data)
test_data <- testing(split)
n_test <- nrow(test_data)

# write train/test files
people %>%
  pull(sample) %>%
  write_lines(str_glue("data/fake_data_train_n_{n_train}.csv.json"))

people %>%
  pull(sample_hashed) %>%
  write_lines(str_glue("fake_data_hashed_train_n_{n_train}.json"))


