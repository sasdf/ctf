#!/bin/bash
#
exec 2>/dev/null
cd /home/john/task
timeout 60 /home/john/task/task.py
