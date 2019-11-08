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

## debug
* debug{"debug": "on"}
  - slot{"debug": "1"}
  - utter_slots

## f1_score
* f1_score
  - action_f1_score

## survey
* survey{"survey": "off"}
  - slot{"survey": "0"}
  - utter_slots

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

## chuck_joke
* chuck_joke
  - action_chuck_joke

## ron_joke
* ron_joke
  - action_ron_joke

## breaking_bad_joke
* breaking_bad_joke
  - action_breaking_bad_joke

## corny_joke
* corny_joke
  - action_corny_joke

## inspiring_quote
* inspiring_quote
  - action_inspiring_quote

## geek_quote
* geek_quote
  - action_geek_quote

## trump_quote
* trump_quote
  - action_trump_quote
