#!/bin/bash
if ! [ -d /usr/local/var/postgres ] &> /dev/null ; then 
  /bin/bash macos_setup/setup_postgres.sh
fi

if ! pg_isready -U admin -d gazettedb ; then
  pg_ctl -D /usr/local/var/postgres start
fi

if ! pip show psycopg2-binary &> /dev/null ; then
  pip install psycopg2-binary==2.8.4
fi

graceful_shutdown() {
  trap - SIGINT SIGTERM # clear the trap
  echo "gracefully shutting down the postgres server..."
  echo "to force a shutdown, press ^C"
  pg_ctl -D /usr/local/var/postgres stop
  exit
}

trap graceful_shutdown SIGINT SIGTERM

/usr/local/bin/python3.8 manage.py migrate

/usr/local/bin/python3.8 manage.py runserver
