#!/bin/bash
#
exec 2>/dev/null
cd /home/harc4/task
timeout 60 /home/harc4/task/task.py
