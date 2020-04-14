## story_greet <!--- The name of the story. It is not mandatory, but useful for debugging. -->
* greet <!--- User input expressed as intent. In this case it represents users message 'Hello'. -->
  - utter_greet <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response 'Hello, how can I help?' -->

## greet 2
* greet
  - utter_greet
* goodbye
  - utter_goodbye
  - action_restart

## story_goodbye
* goodbye
  - utter_goodbye
  - action_restart

## clear
* clear
  - utter_clear
  - action_restart

## feedback
* feedback{"feedback":"positive"}
  - slot{"feedback":"positive"}
  - action_feedback

## f1_score
* f1_score
  - action_f1_score

## story_thanks
* thanks
  - utter_thanks

## story_version
* version
  - utter_version
  - action_version

## chitchat #1
* chitchat
  - utter_chitchat

## chuck_joke greet
* greet
  - utter_greet
* joke{"joke_type": "chuck"}
  - action_chuck

## ron joke
* joke{"joke_type": "chuck"}
  - action_chuck

## chuck_joke 2
* joke
  - utter_ask_joke_type
* joke{"joke_type":"chuck"}
  - action_chuck

## ron_joke prompt
* joke
  - utter_ask_joke_type
* quote{"quote_type":"ron"}
  - action_ron

## ron joke
* joke{"quote_type":"ron"}
  - action_ron

## geek joke
* joke{"joke_type":"geek"}
  - action_geek

## breaking
* quote{"quote_type":"breaking"}
  - action_breaking

## corny_joke greet
* joke
  - utter_ask_joke_type
* joke{"joke_type":"corny"}
  - slot{"joke_type":"corny"}
  - action_corny

## corny
* joke{"joke_type":"corny"}
  - slot{"joke_type":"corny"}
  - action_corny

## inspiring_quote
* quote
  - utter_ask_quote_type
* quote{"quote_type":"inspiring"}
  - slot{"quote_type":"inspiring"}
  - action_inspiring

## inspiring_quote filled
* quote{"quote_type":"inspiring"}
  - action_inspiring

## trump_quote
* quote
  - utter_ask_quote_type
* quote{"quote_type":"trump"}
  - action_trump

## Greet+Inspiring
* greet
    - utter_greet
* quote{"quote_type":"inspiring"}
    - slot{"quote_type":"inspiring"}
    - action_inspiring

## Trump Story
* quote{"quote_type":"trump"}
    - action_trump

## Inspiring+Trump
* quote{"quote_type":"inspiring"}
    - action_inspiring
* quote{"quote_type":"trump"}
    - action_trump

## Trump quote
* quote{"quote_type":"trump"}
    - slot{"quote_type":"trump"}
    - action_trump

## time_from
* time_from
  - action_time_range

## time_range
* time_range
  - action_time_range

## show_slots
* show_slots
  - action_show_slots