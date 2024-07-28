# Note: All data used in this example is synthetic; there is no real data.
# This assumes that an inference server is running set up by llama.cpp.

rm(list=ls())
library(tidyverse)
library(httr2)
library(rlang) # hash
library(conflicted)
set.seed(08544)

# Create people used for testing
age <- 18:45
country <- c("Chad", "Netherlands", "South Korea")
desire <- c("wants a baby", "doesn't want a baby")
testing_books <- expand_grid(age = age, country = country, desire = desire)

testing_books <- testing_books %>%
  mutate(person_id = row_number()) %>%
  mutate(person_id_hash = map_chr(person_id, hash)) %>%
  mutate(book_of_life = str_glue("Person_id is {person_id_hash}, Age is {age}, Country is {country}, Desire is {desire}"))

testing_books <- testing_books %>%
  mutate(person_id = row_number()) %>%
  mutate(person_id_hash = map_chr(person_id, hash)) %>%
  mutate(system_prompt = "You are a smart, helpful AI assistant trained to predict life outcomes. You always answer either 1 for yes or 0 for no. You do not explain your answer.") %>%
  mutate(user_prompt = str_glue("Predict if this person will have a kid in 2021-2023. Person information: {book_of_life}. Answer 1 or 0. Do not explain.  Answer:")) 

testing_books <- testing_books %>% 
  mutate(llama3_prompt = str_glue("<|start_header_id|>system<|end_header_id|>
{system_prompt}<|eot_id|>\n\n<|start_header_id|>user<|end_header_id|>
{user_prompt}<|eot_id|>\n\n<|start_header_id|>assistant<|end_header_id|>
<|eot_id|>")) 

get_response <- function(prompt) {
  
  n_predict <- 10 # number of tokens to return
  n_probs <- 5 # probability of top 5 most probable tokens
  temperature <- 1 # temperature of 0 means deterministic
  # Optional TODO move out of function to save time
  base_url_local_server <- "http://localhost:8080"
  access_token_local_server <- "required_but_not_used"
  endpoint <- "/v1/completions"
  
  req_stub <- request(paste0(base_url_local_server, endpoint)) %>%
    req_headers(
      `Content-Type` = "application/json",
      `Authorization` = paste("Not needed")
    ) %>%
    req_throttle(rate = 120/60) # 120 requests per minute
  
  req <- req_stub %>%
    req_body_json(
      list(
        prompt = prompt,
        n_predict = n_predict,
        n_probs = n_probs, 
        temperature = temperature
      )
    )
  
  # make call
  resp <- req_perform(req)
  
  if (resp_status(resp) != 200) {
    stop("Response Error: ", resp_status(resp))
  }
  
  return(resp)
}

# prepare to do queries
testing_books <- testing_books %>%
  sample_frac() # randomly permute rows

#testing_books <- testing_books %>%
# slice_sample(n = 10)

# do queries
print("Beginning queries")
raw_responses <- map(testing_books$llama3_prompt, get_response)
print("End queries")

# process responses
response_bodies <- map(raw_responses, resp_body_json)

responses <- tibble(
  prompt = map_chr(response_bodies, pluck, "prompt"),
  response = map_chr(response_bodies, pluck, "content"),
  model = map_chr(response_bodies, pluck, "model"),  
  timings = map(response_bodies, pluck, "timings")
) 

if (responses %>% select(model) %>% n_distinct() != 1) {
  stop("All models should be the same")
} else {
  model_str <- responses %>% select(model) %>% distinct() %>% pull()
}

responses <- responses %>% 
  mutate(person_id_hash = str_extract(prompt, "(?<=Person_id is ).*?(?=,)")) %>%
  mutate(prompt_id = row_number(), .before = 1) 

check_response_extract_prediction <- function(response) {
  if (str_starts(response, "assistant")) {
   prediction <- str_extract(response, "(?<=assistant\n\n|assistant\n).*$")
  } else {
    print(paste("response:", response))
    stop("Response does not start with 'assistant'")
  }
  prediction <- as.numeric(prediction)
  if (prediction %in% (c(0,1))) {
    return(prediction)
  } else {
    print(paste("response:", response))
    print(paste("prediction:", prediction))
    stop("Prediction is not 0 or 1")
  } 
}

resp_predictions <- responses %>% 
  mutate(prediction = map_dbl(response, check_response_extract_prediction))

#responses <- responses %>% 
#  unnest_wider(timings)
responses <- responses %>%
  select(-timings)

completion_probabilities <- map(response_bodies, pluck, "completion_probabilities")

make_tibble_completion_probabilities <- function(one_completion_probabilities_list) {
  result <- one_completion_probabilities_list %>%
    # Convert the outer list to a tibble
    enframe(name = "token", value = "content") %>%
    # Unnest the first level
    unnest_wider(content) %>%
    # Unnest the probs list
    unnest_longer(probs) %>%
    # Unnest the tok_str and prob columns
    unnest_wider(probs) 
  return(result)
}

completion_probabilities_tib <- map_dfr(completion_probabilities, make_tibble_completion_probabilities, .id = "prompt_id") 

# Only keep token 5 (that's the prediction)
predictions_tib <- completion_probabilities_tib %>%
  mutate(prompt_id = as.integer(prompt_id)) %>%
  dplyr::filter(token == 5) %>%
  select(prompt_id, tok_str, prob) %>%
  rename(prediction = tok_str, prediction_prob = prob) %>%
  dplyr::filter(prediction %in% c("0", "1"))

responses <- responses %>%
  left_join(predictions_tib, by = "prompt_id") 

# merge age, country, desire from testing_books onto responses
responses_and_inputs <- 
  left_join(responses, testing_books, by = "person_id_hash")

# Plot the results

# data to plot
data_to_plot <- responses_and_inputs %>%
  dplyr::filter(prediction == "1") %>%
  select(person_id_hash, age, country, desire, prediction, prediction_prob)

# plot
p <- ggplot(data_to_plot, aes(age, prediction_prob)) +
  geom_point() +
  facet_grid(country ~ desire) +
  labs(title = model_str,
       x = "Age",
       y = "Predicted probability of having a kid",
       tag = format(Sys.time(), "%Y-%m-%d %H:%M")) +
  theme(plot.tag = element_text(size = 8, color = "gray50", hjust = 1, vjust = 1),
        plot.tag.position = c(1, 0))

file_prefix <- "~/prefer_prepare/fertility_data_sim/"
ggsave(paste0(file_prefix, model_str, "_notuning.png"), plot = p)
print(paste("Saved plot", paste0(file_prefix, model_str, "_notuning.png"))
print("End of file")
