#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
RUN git clone https://github.com/apache/incubator-age age
RUN git clone https://github.com/apache/age-viewer age-viewer

# changed path in dockerfile (age-viewer)
ADD ./age-viewer/frontend /app/frontend
ADD ./age-viewer/backend /app/backend

COPY age-viewer/docker-entrypoint.sh /usr/local/bin/

RUN docker-compose up

RUN python3 data-generation/python/src/create_nodes.py

# sudo apt-get install build-essential libreadline-dev zlib1g-dev flex bison
# make PG_CONFIG=/path/to/postgres/bin/pg_config install

# select * from pg_available_extensions where installed_version is not null ;
