#!/bin/bash

# This script will quit on the first error that is encountered.
set -e

CIRCLE=$1

DEPLOY_DATE=`date "+%FT%T%z"`
SECRET=$(openssl rand -base64 58 | tr '\n' '_')

heroku config:set --app=analysocial \
NEW_RELIC_APP_NAME='analysocial' \
ADMIN_EMAIL="jessamyn.smith@gmail.com" \
ADMIN_NAME="Analysocial" \
DJANGO_SETTINGS_MODULE=analysocial.settings \
DJANGO_ENABLE_SSL=1 \
DJANGO_SECRET_KEY="$SECRET" \
DEPLOY_DATE="$DEPLOY_DATE" \
> /dev/null

if [ $CIRCLE ]
then
    git push https://heroku:$HEROKU_API_KEY@git.heroku.com/analysocial.git master
else
    git push heroku master
fi

heroku run python manage.py migrate --noinput --app analysocial
