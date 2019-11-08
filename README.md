# Jokebot - Rasa X Demo Bot

This is a Rasa X demo bot. You can try the bot out at [http://gstephens.org/jokebot](http://gstephens.org/jokebot).

The bot can be run under the lighterweight local Rasa X install or the full Rasa X docker stack. These instructions run the lightweight Rasa X in a Docker container.

You can run your own copy of the bot using these steps:

```
git clone
export RASA_X_VERSION=0.22.1
export RASA_SDK_VERSION=1.4.0
docker build --build-arg vers=${RASA_X_VERSION} -t rasax:${RASA_X_VERSION} .
docker-compose -f docker-compose-local.yml up -d
docker-compose -f docker-compose-local.yml logs rasa-x | grep password
```

# Scripts

The project includes the following scripts:

| Script              | Usage                              |
| ------------------- | ---------------------------------- |
| build.sh            | Build Rasa Docker container        |
| train.sh            | Train the model                    |
| entrypoint.sh       | Docker entrypoint for full Rasa X  |
| entrypoint_local.sh | Docker entrypoint for local Rasa X |

# Rasa X & Rasa Version Combinations

| Rasa X |  Rasa  | Rasa SDK |
| :----: | :----: | :------: |
| 0.22.1 | 1.4.3  |  1.4.0   |
| 0.21.5 | 1.3.9  |  1.3.3   |
| 0.21.4 | 1.3.9  |  1.3.3   |
| 0.21.3 | 1.3.9  |  1.3.3   |
| 0.20.5 | 1.2.11 |  1.2.0   |
| 0.20.0 | 1.2.5  |  1.2.0   |

