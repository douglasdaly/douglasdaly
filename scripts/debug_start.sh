#!/bin/bash

# - Variables
let WORKERS=1

# - Start Gunicorn Server
echo "[INFO] Starting gunicorn on debug application..."
exec gunicorn config.debug_wsgi:application \
    --chdir douglasdaly/ \
    --bind 0.0.0.0:8000 \
    --workers $WORKERS \
    --log-level=info