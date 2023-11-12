#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

exec gunicorn --bind '[::]:8000' --worker-tmp-dir /dev/shm --workers 3 energokodros.wsgi:application