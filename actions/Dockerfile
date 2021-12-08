# Dockerfile from https://hub.docker.com/r/rasa/rasa-sdk/dockerfile
# Git Repo from https://github.com/RasaHQ/rasa-sdk
#FROM python:3.6-slim
#FROM rasa/rasa-sdk:${RASA_SDK_VERSION}
FROM rasa/rasa-sdk:2.8.2
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Americas/Los_Angeles

SHELL ["/bin/bash", "-c"]

#RUN echo $UID
USER root
RUN ls -l /app

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  vim \
  emacs \
  build-essential && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
#  mkdir /app

RUN ls -l /

USER 1001
#RUN mkdir /app

WORKDIR /app

# Copy as early as possible so we can cache ...
COPY requirements.txt .

RUN python -m pip install --upgrade pip
USER root
RUN pip install -r requirements.txt --no-cache-dir
USER 1001

COPY . .

#RUN pip install -e . --no-cache-dir

VOLUME ["/app/actions"]

EXPOSE 5055

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions"]