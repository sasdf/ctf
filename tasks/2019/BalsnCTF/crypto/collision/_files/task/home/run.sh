#!/bin/bash
#
exec 2>/dev/null
cd /home/collision/task
timeout 60 /home/collision/task/main.py
