#!/bin/bash

IP=${1:-127.0.0.1}

rm -f dump
for i in `seq 1 64`; do
    ncat "$IP" 37896 --recv-only >> dump
done
