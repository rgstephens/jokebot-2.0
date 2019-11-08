#!/bin/bash
export RASA_X_VERSION=0.22.1
export RASA_SDK_VERSION=1.4.0
docker build --build-arg vers=${RASA_X_VERSION} -t rasax:${RASA_X_VERSION} .
