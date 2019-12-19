# Dockerfile from https://hub.docker.com/r/rasa/rasa-sdk/dockerfile
# Git Repo from https://github.com/RasaHQ/rasa-sdk
#FROM python:3.6-slim
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

SHELL ["/bin/bash", "-c"]

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  build-essential && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
  mkdir /app

WORKDIR /app

# Copy as early as possible so we can cache ...
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN pip install -e . --no-cache-dir

VOLUME ["/app/actions"]

EXPOSE 5055

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions.actions"]