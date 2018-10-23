#!/bin/bash

# - Variables
PROCESSORS=$(grep -c ^processor /proc/cpuinfo)
let WORKERS=(2*PROCESSORS)+1

# - Setup Logs
touch logs/gunicorn.log
touch logs/access.log
tail -n 0 -f logs/*.log &

# - Start Gunicorn Server
echo "[INFO] Starting gunicorn on debug application..."
exec gunicorn config.local_wsgi:application \
    --chdir douglasdaly/ \
    --bind 0.0.0.0:8000 \
    --workers $WORKERS \
    --log-level=info