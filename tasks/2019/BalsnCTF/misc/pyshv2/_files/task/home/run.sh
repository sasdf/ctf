#!/bin/bash
#
exec 2>/dev/null
cd /home/pyshv2/task
timeout 60 /home/pyshv2/task/server.py
