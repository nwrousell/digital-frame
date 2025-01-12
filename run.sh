#!/bin/bash

cd /home/noah/digital-frame
source env/bin/activate

nohup sudo startx -- -ac &
export DISPLAY=:0

sleep 5
python main.py