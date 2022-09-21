#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

RUN git clone https://github.com/apache/incubator-age age

# sudo apt-get install build-essential libreadline-dev zlib1g-dev flex bison
# make PG_CONFIG=/path/to/postgres/bin/pg_config install

# select * from pg_available_extensions where installed_version is not null ;
