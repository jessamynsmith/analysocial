#!/bin/bash

# This script will quit on the first error that is encountered.
set -e

#!/bin/bash
YEAR=2006
while [ $YEAR -lt 2017 ]; do
    heroku run python manage.py email_posts_to_users --year=$YEAR
    let YEAR=YEAR+1
done
