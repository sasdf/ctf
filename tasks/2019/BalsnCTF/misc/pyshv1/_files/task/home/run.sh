#!/bin/bash
#
exec 2>/dev/null
cd /home/pyshv1/task
timeout 60 /home/pyshv1/task/server.py
