#!/bin/bash

docker build -t balsn-dlog . && \
docker run --rm -it --name test -p 127.0.0.1:27492:27492/tcp balsn-dlog
