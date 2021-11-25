#!/bin/bash

docker build -t balsn-trinity .
docker run --rm -it --name test -p 127.0.0.1:27490:27490/tcp balsn-trinity
