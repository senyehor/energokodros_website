#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

exec gunicorn --bind "[::]:${APP_PORT}" --worker-tmp-dir /dev/shm --workers 3 energokodros.wsgi:application