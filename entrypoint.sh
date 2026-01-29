#!/usr/bin/env bash
set -e

# wait for DATABASE_URL to be set
if [ -z "${DATABASE_URL}" ]; then
  echo "WARNING: DATABASE_URL not set, skipping migrate/collectstatic"
else
  echo "Running migrations and collecting static files..."
  # try to run migrations; retry a few times if DB not ready
  n=0
  until [ $n -ge 10 ]
  do
    python manage.py migrate && break
    n=$((n+1))
    echo "migrate failed, retrying ($n)..."
    sleep 3
  done

  python manage.py collectstatic --noinput || true
fi

# exec the passed command (gunicorn)
exec "$@"
