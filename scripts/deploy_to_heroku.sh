#!/bin/bash

# This script will quit on the first error that is encountered.
set -e

CIRCLE=$1

DEPLOY_DATE=`date "+%FT%T%z"`
SECRET=$(openssl rand -base64 58 | tr '\n' '_')

heroku config:set --app=escape-from-fb \
NEW_RELIC_APP_NAME='escape_from_fb' \
ADMIN_EMAIL="jessamyn.smith@gmail.com" \
ADMIN_NAME="escape from fb" \
DJANGO_SETTINGS_MODULE=escape_from_fb.settings \
DJANGO_SECRET_KEY="$SECRET" \
DEPLOY_DATE="$DEPLOY_DATE" \
> /dev/null

if [ $CIRCLE ]
then
    git fetch origin --unshallow
    git push git@heroku.com:escape_from_facebook.git $CIRCLE_SHA1:refs/heads/master
else
    git push heroku master
fi

heroku run python manage.py migrate --noinput --app=escape-from-fb
