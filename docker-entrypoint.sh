#!/usr/bin/env bash

set -u
set -e

cd /app

export PYTHONPATH=authstatus

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
