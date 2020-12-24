validate:
	rasa data validate --debug

cross-validate:
	rasa test nlu -f 3 --cross-validation

train:
	time rasa train
