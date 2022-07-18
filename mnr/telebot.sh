#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

if pgrep -f check_status.py > /dev/null
then
    echo "$(date +%y-%m-%d-%H-%M-%S) check_status.py is alive. Doing nothing."
else
    echo "No check_status.py. Kickstarting..."
    cd /home/dooky/mnr/miner
    python3 check_status.py &
    cd /
    echo "check_status.py now is running"
fi
