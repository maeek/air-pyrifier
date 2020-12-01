#!/bin/bash

docker run --rm -it \
  --name lan-airserver \
  -v /projects/air-pyrifier/airserver:/srv \
  -u 1000:1000 \
  -p 8765:8765 \
  airserver

