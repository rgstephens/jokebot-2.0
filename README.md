# Jokebot - Rasa X Demo Bot

This is a Rasa X demo bot. You can try the bot out at [http://gstephens.org/jokebot](http://gstephens.org/jokebot).

The chatbot is setup to run under the lighterweight local Rasa X install in a Docker container with `docker-compose`.

Update the version numbers in the `.env` file. You can find the version info in the tags for the [Docker Hub Images](https://hub.docker.com/u/rasa).

```
RASA_X_VERSION=0.26.3
RASA_VERSION=1.8.2
RASA_SDK_VERSION=1.8.1
```

You can run your own copy of the bot using these steps:

```sh
git clone https://github.com/rgstephens/jokebot.git
cd jokebot
docker-compose build --no-cache
docker-compose run rasa-x rasa train
docker-compose up -d
docker-compose logs rasa-x | grep password
```

## Ports

The `docker-compose.yml` uses the default ports which can be over-ridden. This is partcularly useful if you want to run multiple chatbots on the same host.

- `5005` - Rasa port (point your client here)
- `5002` - Rasa X UI

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

There is a [Rasa Compatibility Matrix](https://rasa.com/docs/rasa-x/changelog/compatibility-matrix/).

The docker hub images are here:

- [rasa tags](https://hub.docker.com/r/rasa/rasa/tags)
- [rasa-x tags](https://hub.docker.com/r/rasa/rasa-x/tags)
- [rasa-sdk tags](https://hub.docker.com/r/rasa/rasa-sdk/tags)

## Training Times

| Rasa Version | Pipeline                  | Time |
| :----------: | ------------------------- | :--: |
|     1.8      | EmbeddingIntentClassifier | 1:07 |
|     1.8      | DIETClassifier            | 2:10 |

## ToDo

- Brainy quote, `https://github.com/Hemil96/Brainyquote-API`
- Github Actions pipeline
- Google Assistant integration
- NLU test data
- Core test data
- rasa validate
- Support [multi-intents](https://blog.rasa.com/how-to-handle-multiple-intents-per-input-using-rasa-nlu-tensorflow-pipeline/?_ga=2.50044902.1771157212.1575170721-2034915719.1563294018)
- travis testing with carbon bot style test results table

## New Features

**Jan 2021:**

- GitHub actions
  - Build actions docker image
- Creed quotes
- Kanye quotes, `https://api.kanye.rest/?format=text`
- Random jokes, `http://api.icndb.com/jokes/random`

## 2.0 Migration

2.0 Migration Steps:

```
mv data data-1.0
mkdir -p data
rasa data convert nlu -f yaml --data data-1.0 --out data
rasa data convert core -f yaml --data data-1.0 --out data
```

## Test Curl

```
curl --location --request POST 'http://localhost:5055/webhook' \
--data-raw '{      
  "next_action": "action_kanye",
  "sender_id": "postman",
  "tracker": {
    "sender_id": "default",
    "slots": {},
    "latest_message": {},
    "latest_event_time": 1535092548.4191391,
    "followup_action": "action_listen",
    "events": []
  },
  "domain": {
    "config": {},
    "intents": [],
    "entities": [],
    "slots": {}
  }
}'
```

```
curl --location --request POST 'http://rasa-production:5005/webhooks/rest/webhook' --header 'Content-Type: application/x-www-form-urlencoded' --data-raw '{"sender": "postman","message": "hello" }'
curl --location --request POST 'http://localhost/webhooks/rest/webhook' --header 'Content-Type: application/x-www-form-urlencoded' --data-raw '{"sender": "postman","message": "hello" }'
curl --location --request POST 'http://localhost:5005/webhooks/rest/webhook' --header 'Content-Type: application/x-www-form-urlencoded' --data-raw '{"sender": "postman","message": "hello" }'
```