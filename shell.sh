#!/bin/bash
export RASA_VERS=1.4.3-full
export RASA_MODEL_SERVER="https://localhost:5002"
docker run -v $(pwd):/app rasa/rasa:${RASA_VERS} shell --model /app/models/$(ls models)
