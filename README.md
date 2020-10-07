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

- [rasa tags](https://hub.docker.com/r/rasa/rasa/tags)
- [rasa-x tags](https://hub.docker.com/r/rasa/rasa-x/tags)
- [rasa-sdk tags](https://hub.docker.com/r/rasa/rasa-sdk/tags)

| Rasa X |  Rasa  | Rasa SDK |
| :----: | :----: | :------: |
| 0.27.4 | 1.9.5  |  1.9.0   |
| 0.26.3 | 1.8.2  |  1.8.1   |
| 0.25.1 | 1.7.0  |  1.7.0   |
| 0.24.6 | 1.6.4  |  1.6.1   |
| 0.23.5 | 1.5.3  |  1.5.2   |
| 0.23.3 | 1.5.1  |  1.5.0   |
| 0.22.1 | 1.4.3  |  1.4.0   |
| 0.21.5 | 1.3.9  |  1.3.3   |
| 0.21.4 | 1.3.9  |  1.3.3   |
| 0.21.3 | 1.3.9  |  1.3.3   |
| 0.20.5 | 1.2.11 |  1.2.0   |
| 0.20.0 | 1.2.5  |  1.2.0   |

## Training Times

| Rasa Version | Pipeline                  | Time |
| :----------: | ------------------------- | :--: |
|     1.8      | EmbeddingIntentClassifier | 1:07 |
|     1.8      | DIETClassifier            | 2:10 |

## ToDo

- Use featurized slots
- Kanye quote, `https://api.kanye.rest/?format=text`
- Random joke endpoint, `http://api.icndb.com/jokes/random`
- Google Assistant integration
- NLU test data
- Core test data
- rasa validate
- Support [multi-intents](https://blog.rasa.com/how-to-handle-multiple-intents-per-input-using-rasa-nlu-tensorflow-pipeline/?_ga=2.50044902.1771157212.1575170721-2034915719.1563294018)
- travis testing with carbon bot style test results table

### Creed Quotes

- I wanna do a cartwheel. But real casual like. Not enough to make a big deal out of it, but I know everyone saw it. One stunning, gorgeous cartwheel.
- I’ve been involved in a number of cults, both a leader and a follower. You have more fun as a follower, but you make more money as a leader.
- Just pretend like we're talking until the cops leave.
- I already won the lottery. I was born in the US of A baby. And as backup I have a Swiss passport.
- The Taliban in the worst. Great heroin though.
- I run a small fake-ID company from my car with a laminating machine that I swiped from the Sheriff’s station.
-
- Ryan, you told Toby that Creed has a distinct old man smell
- Creed quotes - I know exactly what he's talking about, I sprout mung beans on a damp paper towel in my desk drawer, very nutritious but they smell like death

https://www.theodysseyonline.com/best-creed-bratton-quotes-the-office

## 2.0 Migration

2.0 Migration Steps:

```
mv data data-1.0
mkdir -p data
rasa data convert nlu -f yaml --data data-1.0 --out data
rasa data convert core -f yaml --data data-1.0 --out data
```