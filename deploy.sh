#!/bin/bash
# this is an easy (re)deploy script for running a lflux instance w/ pbundler, gunicorn and supervisord

sh ./update_dependencies.sh
pbundle # update dependencies.
pbundle run ./lfluxproject/manage.py collectstatic --noinput
pbundle run ./lfluxproject/manage.py syncdb
pbundle run ./lfluxproject/manage.py migrate
pbundle run ./lfluxproject/manage.py compilemessages
X=`pbundle run printenv SUPERVISOR_NAME`
pbundle run sudo supervisorctl restart $X
