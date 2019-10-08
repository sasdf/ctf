#!/bin/bash
#
exec 2>/dev/null
cd /home/pyshv3/task
timeout 60 /home/pyshv3/task/server.py
