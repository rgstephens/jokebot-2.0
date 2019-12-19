# Jokebot - Rasa X Demo Bot

This is a Rasa X demo bot. You can try the bot out at [http://gstephens.org/jokebot](http://gstephens.org/jokebot).

The bot can be run under the lighterweight local Rasa X install or the full Rasa X docker stack. These instructions run the lightweight Rasa X in a Docker container.

Review the version numbers in the `.env` and update.

You can run your own copy of the bot using these steps:

```sh
git clone https://github.com/rgstephens/jokebot.git
cd jokebot
docker-compose run rasa-x rasa train
docker-compose up -d
docker-compose logs rasa-x | grep password
```

# Update Server

To update the server, update the version numbers in the `.env` and enter the following commands

```sh
sudo docker-compose down
docker-compose up -d
docker-compose logs rasa-x | grep password
```

# Training

Local training using your local python environment (or conda/venv)

```sh
docker-compose run rasa-x rasa train
```

# Testing

After training the model, run the command:

```sh
docker-compose run rasa-x rasa test nlu -u test/test_data.md --model models/$(ls models)
docker-compose run rasa-x rasa test core --stories test/test_stories.md
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
| 0.23.5 | 1.5.3  |  1.5.2   |
| 0.23.3 | 1.5.1  |  1.5.0   |
| 0.22.1 | 1.4.3  |  1.4.0   |
| 0.21.5 | 1.3.9  |  1.3.3   |
| 0.21.4 | 1.3.9  |  1.3.3   |
| 0.21.3 | 1.3.9  |  1.3.3   |
| 0.20.5 | 1.2.11 |  1.2.0   |
| 0.20.0 | 1.2.5  |  1.2.0   |

## ToDo

* Use featurized slots
* Kanye quote, `https://api.kanye.rest/?format=text`
* Random joke endpoint, `http://api.icndb.com/jokes/random`
* Google Assistant integration
* NLU test data
* Core test data
* rasa validate
* Support [multi-intents](https://blog.rasa.com/how-to-handle-multiple-intents-per-input-using-rasa-nlu-tensorflow-pipeline/?_ga=2.50044902.1771157212.1575170721-2034915719.1563294018)
