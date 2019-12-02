# Jokebot - Rasa X Demo Bot

This is a Rasa X demo bot. You can try the bot out at [http://gstephens.org/jokebot](http://gstephens.org/jokebot).

The bot can be run under the lighterweight local Rasa X install or the full Rasa X docker stack. These instructions run the lightweight Rasa X in a Docker container.

You can run your own copy of the bot using these steps:

```
git clone https://github.com/rgstephens/jokebot.git
export RASA_X_VERSION=0.23.1
export RASA_VERSION=1.5.1-full
export RASA_SDK_VERSION=1.5.1
docker build --build-arg vers=${RASA_X_VERSION} -t rasax:${RASA_X_VERSION} .
docker-compose -f docker-compose-local.yml up -d
docker-compose -f docker-compose-local.yml logs rasa-x | grep password
```

# Full Server Setup

* Follow [Deploy to Server](https://rasa.com/docs/rasa-x/deploy/) instructions to setup new Rasa X

# Update Server

To update the server:

```sh
sudo docker-compose down
git pull
export RASA_X_VERSION=1.5.1-full
export RASA_SDK_VERSION=1.5.1
sudo docker build --build-arg vers=${RASA_X_VERSION} -t rasax:${RASA_X_VERSION} .
docker pull rasa/rasa:${RASA_VERSION}
docker run -v $(pwd):/app rasa/rasa:${RASA_VERSION} train --config /app/config.yml --out /app/models --domain /app/domain.yml --data /app/data/training /app/data/stories -vv
docker-compose -f docker-compose-local.yml up -d
docker-compose -f docker-compose-local.yml logs rasa-x | grep password
```

# Training

Local training using your local python environment (or conda/venv)

```sh
rasa train
```

To train with Docker:

```sh
export RASA_X_VERSION=1.5.1-full
docker run -v $(pwd):/app rasa/rasa:${RASA_X_VERSION} train --config /app/config.yml --out /app/models --domain /app/domain.yml --data /app/data/training /app/data/stories -vv
```

# Testing

After training the model, run the command:

```sh
docker run -v $(pwd):/app rasa/rasa:${RASA_VERSION} test nlu -u test/test_data.md --model models/$(ls models)
docker run -v $(pwd):/app rasa/rasa:${RASA_VERSION} test core --stories test/test_stories.md
```

# Rasa Interactive Shell

```sh
docker run -v $(pwd):/app rasa/rasa:${RASA_VERSION} run actions --actions actions.actions
docker-compose up app -d
docker run -it -v $(pwd):/app rasa/rasa:${RASA_VERSION} shell --debug
```

With Docker:

```sh
export RASA_X_VERSION=1.5.1-full
export RASA_MODEL_SERVER="https://localhost:5002"
docker run --it --rm --network=$(basename `pwd`)_default -v $(pwd):/app rasa/rasa:${RASA_X_VERSION} shell --model /app/models/$(ls models) --endpoints endpoints_local.yml
```

# Scripts

The project includes the following scripts:

| Script              | Usage                              |
| ------------------- | ---------------------------------- |
| entrypoint.sh       | Docker entrypoint for full Rasa X  |
| entrypoint_local.sh | Docker entrypoint for local Rasa X |

# Rasa X & Rasa Version Combinations

| Rasa X |  Rasa  | Rasa SDK |
| :----: | :----: | :------: |
| 0.23.1 | 1.5.1  |  1.5.0   |
| 0.22.1 | 1.4.3  |  1.4.0   |
| 0.21.5 | 1.3.9  |  1.3.3   |
| 0.21.4 | 1.3.9  |  1.3.3   |
| 0.21.3 | 1.3.9  |  1.3.3   |
| 0.20.5 | 1.2.11 |  1.2.0   |
| 0.20.0 | 1.2.5  |  1.2.0   |

## ToDo

* Use featurized slots
* Ask for joke and prompt for joke type
* Ask for quote and prompt for joke type
* Kanye quote, `https://api.kanye.rest/?format=text`
* Random joke endpoint, `http://api.icndb.com/jokes/random`
* Google Assistant integration
* Android access via [Aimybox](https://blog.rasa.com/how-to-build-a-mobile-voice-assistant-with-open-source-rasa-and-aimybox/ )
* NLU test data
* Core test data
* rasa validate
