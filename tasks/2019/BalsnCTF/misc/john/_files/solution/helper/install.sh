#!/bin/bash
sudo apt-get update
sudo apt-get install tmux tcpdump python3-pip
pip3 install --pre scapy[basic]
sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST --dport 5452 -j DROP
