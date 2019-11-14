#!/bin/bash
#export RASA_VERS=1.2.11-full
export RASA_VERS=1.4.3-full
docker run -v $(pwd):/app rasa/rasa:${RASA_VERS} train --config /app/config.yml --out /app/models --domain /app/domain.yml --data /app/data/training /app/data/stories -vv
# docker run -v $(pwd):/app rasa/rasa:${RASA_VERS} shell --model /app/models/$(ls models)
# --config /app/config.yml --out /app/models --domain /app/domain.yml --data /app/data/training /app/data/stories -vv
#export RASA_VERS=latest-full
#docker run -v $(pwd):/app rasa/rasa:${RASA_VERS} train --config /app/data/config_default.yml --out /app/models --domain /app/data/domain.yml --data /app/data/training /app/data/stories
#docker run -v $(pwd)/data:/app/data rasa/rasa:${RASA_VERS} train --config /app/data/config.yml --out /app/data/models --domain /app/data/domain.yml --data /app/data/training /app/data/stories

