#!/bin/bash

cd /path/to/digital-frame # TODO: update this path
source env/bin/activate

nohup sudo startx -- -ac &
export DISPLAY=:0

sleep 5
python main.py
