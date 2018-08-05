#!/bin/sh

mkdir -p build
gcc -no-pie -S task.c -o build/task.s
python3 scramble.py build/task.s > build/scrambled.s
gcc -no-pie build/scrambled.s -o build/task
# strip build/task
mkdir -p ../task
cp build/task ../task/task
