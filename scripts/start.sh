#!/bin/bash

# - Variables
PROCESSORS=$(grep -c ^processor /proc/cpuinfo)
let WORKERS=(2*PROCESSORS)+1

# - Setup Logs
#touch /var/logs/gunicorn/gunicorn.log
#touch /var/logs/gunicorn/access.log
#tail -n 0 -f logs/*.log &

# - Start Gunicorn Server
exec gunicorn config.wsgi:application \
    --chdir douglasdaly/ \
    --bind 0.0.0.0:8000 \
    --workers $WORKERS \
    --log-level=info

#    --log-file=/var/logs/gunicorn/gunicorn.log \
#    --access-logfile=/var/logs/gunicorn/access.log