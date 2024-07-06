# Note: All data used in this example is synthetic; there is no real data.
# This assumes that an inference server is running set up by llama.cpp.

rm(list=ls())
library(tidyverse)
library(httr2)
set.seed(08544)

filename <- "~/Princeton Dropbox/Matthew Salganik/prefer_prepare/fertility_data_sim/fake_data_for_ft_n=10.csv"
eval_set <- read_csv(filename)

get_response <- function(prompt) {
  
  n_predict <- 10 # number of tokens to return
  n_probs <- 5 # probability of top 5 most probable tokens
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
        n_probs = n_probs
      )
    )
  
  # make call
  resp <- req_perform(req)
  
  if (resp_status(resp) != 200) {
    stop("Response Error: ", resp_status(resp))
  }
  
  return(resp)
}


# do queries
print("Beginning queries")
responses <- map(eval_set$text, get_response)
print("End queries")

response_bodies <- map(responses, resp_body_json)
responses_content <- map_chr(response_bodies, pluck, "content")

write_csv(as_tibble(responses_content), "responses_content.csv")