#!/bin/bash
graceful_shutdown() {
  trap - SIGINT SIGTERM # clear the trap
  echo "gracefully shutting down the postgres server..."
  echo "to force a shutdown, press ^C"
  pg_ctl -D /usr/local/var/postgres stop
  exit
}

trap graceful_shutdown SIGINT SIGTERM

if ! command -v initdb &> /dev/null
then
    echo "command initdb could not be found. Install postgresql to continue."
    echo "To install with homebrew, run: brew install postgresql@15"
    echo "If the problem persists, ensure it is added to your PATH: brew link postgresql@15 --force"
    exit
fi

# make and grant permissions to postgres db location
sudo mkdir -p /usr/local/var/postgres
sudo chmod 700 /usr/local/var/postgres
sudo chown $USER /usr/local/var/postgres/.

# initialize postgres db if it doesn't exist
if ! [ $(psql -lqt | cut -d \| -f 1 | grep -qw gazettedb) ] ; then
  initdb --username=admin /usr/local/var/postgres
fi

# set up postgres database
# start the server
# sudo -u $USER brew services start postgresql@15
# initdb --username=admin /usr/local/var/postgres
pg_ctl -D /usr/local/var/postgres start
  
# create the database itself
psql --username=admin postgres -c "CREATE DATABASE gazettedb;"

# set up postgres user

# psql -U admin postgres -c "CREATE USER admin WITH PASSWORD 'password';"

# query="ALTER ROLE admin SET client_encoding TO 'utf8';"
# query="$query ALTER ROLE admin SET default_transaction_isolation TO 'read committed';"
# query="$query ALTER ROLE admin SET timezone TO 'UTC';"
# psql -U admin postgres -c $query

# grant postgres user privileges to db
psql --username=admin postgres -c "GRANT ALL PRIVILEGES ON DATABASE gazettedb TO admin;"
psql --username=admin postgres -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;"
# try GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <user>; ?
# from https://stackoverflow.com/questions/62472371/psycopg2-errors-insufficientprivilege-permission-denied-for-relation-django-mig
