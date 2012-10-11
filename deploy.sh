#!/bin/bash
# this is an easy (re)deploy script for running a lflux instance w/ pbundler, gunicorn and supervisord

pbundle # update dependencies.
pbundle run ./lfuxproject/manage.py collectstatic --noinput
pbundle run ./lfluxproject/manage.py migrate
X=`pbundle run printenv SUPERVISOR_NAME`
pbundle run sudo supervisorctl restart $X
