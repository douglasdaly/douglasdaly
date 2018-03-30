#!/bin/bash

# - Variables
PROCESSORS=$(grep -c ^processor /proc/cpuinfo)
let WORKERS=(2*PROCESSORS)+1

# - Setup Logs
touch logs/gunicorn.log
touch logs/access.log
tail -n 0 -f logs/*.log &

# - Start Gunicorn Server
exec gunicorn config.wsgi:application \
    --chdir douglasdaly/ \
    --bind 0.0.0.0:8000 \
    --workers $WORKERS \
    --log-level=info \
    --log-file=logs/gunicorn.log \
    --access-logfile=logs/access.log