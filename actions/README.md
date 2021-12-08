Docker Hub [image](https://hub.docker.com/r/stephens/jokebot/tags?page=1&ordering=last_updated)

Notes on building the action agent image:

- Setup build using [rasa-action-server-gha](https://github.com/RasaHQ/rasa-action-server-gha)

# Local Action Agent Build

```sh
cd actions
docker build -t stephens/jokebot:test .
docker tag stephens/jokebot:test stephens/jokebot:1.0.2
```
