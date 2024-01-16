#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
python manage.py migrate --noinput
exec gunicorn energokodros.wsgi:application -c "${APP_DIR}/gunicorn.conf.py"
