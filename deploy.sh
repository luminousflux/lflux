#!/bin/bash
# this is an easy (re)deploy script for running a lflux instance w/ pbundler, gunicorn and supervisord

pbundle # update dependencies.
pbundle run ./manage.py collectstatic --noinput
pbundle run ./manage.py migrate
sudo supervisorctl restart `echo $SUPERVISOR_NAME`
echo $SUPERVISOR_NAME
