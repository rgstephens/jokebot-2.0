# This file is for local testing of Rasa X (not server deployment)
# . .env
# docker build --build-arg vers=${RASA_X_VERSION} -t rasax:${RASA_X_VERSION} .
# docker build --build-arg vers=0.22.1 -t rasax:0.22.1 .
# docker build --no-cache --build-arg vers=0.21.5 -t rasax:0.21.5 .
# docker build --no-cache --build-arg vers=${RASA_X_VERSION} -t rasax:${RASA_X_VERSION} .
# docker-compose -f docker-compose-local.yml up
#FROM ubuntu:16.04
FROM python:3.6

ARG vers

RUN echo "vers: $vers"

RUN if [ "$vers" != "stable" ] ; then echo rasax==$vers ; else echo rasax=stable ; fi

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
      wget \
      curl \
      sudo \
      python

RUN curl -sSL -k "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py

# install rasa
#RUN pip install rasa-x==$vers --extra-index-url https://pypi.rasa.com/simple
RUN if [ "$vers" != "stable" ] ; then pip install rasa-x=="$vers" --extra-index-url https://pypi.rasa.com/simple ; else pip install rasa-x --extra-index-url https://pypi.rasa.com/simple ; fi

VOLUME ["/app"]
WORKDIR /app

COPY ./.env .

# expose port for rasa server
EXPOSE 5005

# expose port for rasa X server
EXPOSE 5002

# expose port for jupyter notebook
EXPOSE 8888
# expose port for ssh
EXPOSE 22

COPY ./entrypoint-local.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#RUN ls -l /
#RUN ls -l
#CMD jupyter notebook --ip 0.0.0.0 --allow-root --port 8888 --no-browser
#CMD ["/usr/sbin/sshd", "-D"]
#CMD ["rasa", "x", "--no-prompt", "--endpoints", "endpoints.yml", "--data", "data", "--credentials", "credentials.yml"]
ENTRYPOINT ["/entrypoint.sh"]