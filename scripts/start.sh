#!/bin/bash

# Start Gunicorn Server
echo Starting Gunicorn

exec gunicorn config.wsgi:application \
    --chdir douglasdaly/ \
    --bind 0.0.0.0:8000 \
    --workers 3
