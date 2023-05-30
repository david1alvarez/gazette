#!/bin/bash
if ! [ -d /usr/local/var/postgres ] &> /dev/null ; then 
  /bin/bash macos_setup/setup_postgres.sh
fi

if ! pg_isready -U admin -d gazettedb ; then
  pg_ctl -D /usr/local/var/postgres start
fi

if ! pip show psycopg2-binary &> /dev/null ; then
  pip3 install -q -r requirements.txt
fi

graceful_shutdown() {
  trap - SIGINT SIGTERM # clear the trap
  echo "gracefully shutting down the postgres server..."
  echo "to force a shutdown, press ^C"
  pg_ctl -D /usr/local/var/postgres stop
  exit
}

trap graceful_shutdown SIGINT SIGTERM

python3 manage.py migrate

python3 manage.py runserver
open -a "Google Chrome" http://127.0.0.1:8000/admin
