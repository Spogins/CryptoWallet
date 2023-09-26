#!/bin/sh

if [ "$DATABASE" = 'postgres' ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#sudo systemctl start rabbitmq-server
#sudo systemctl enable rabbitmq-server
#alembic init -t async migrations
#alembic revision --autogenerate -m "migration"
#alembic upgrade head
#
#
#python init_scripts.py


#make migration
make migrate

make init_scripts



exec "$@"