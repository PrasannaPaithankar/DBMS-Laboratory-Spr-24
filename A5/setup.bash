#!/bin/usr/bash

if [ ! -d ./Solr ]; then
    mkdir -p ./solr
    chmod a+rwx ./solr
fi

sudo docker compose up
