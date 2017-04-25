analysocial
=========

Django app for Analysocial
https://analysocial.herokuapp.com/

Development
-----------

Fork the project on github and git clone your fork, e.g.:

    git clone https://bitbucket.com/<username>/analysocial.git

Create a virtualenv using Python 3 and install dependencies. I recommend getting python3 via [homebrew](http://brew.sh/), then installing [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation) to that python. NOTE! You must change 'path/to/python3'
to be the actual path to python3 on your system.

    mkvirtualenv analysocial --python=/path/to/python3
    pip install -r requirements.txt
    
You may want to set up an alias for making python3 virtualenvs, e.g. in .bashrc:

     alias mkvirtualenv3='mkvirtualenv --python=/usr/local/bin/python3'
    
Ensure node is installed. This can be done via homebrew:

    brew install node
    
Install javascript dependencies:

    npm install
    
Set environment variables as needed. I recommend putting the exports at the end of your ~/.virtualenvs/analysocial/bin/activate so they are always available when in your virtualenv. You need to substitute appropriate values for all <CONFIGURABLE_ITEMS>.

    export DJANGO_SETTINGS_MODULE=analysocial.settings
    export DJANGO_ENABLE_SSL=0
    export DJANGO_DEBUG=1
    export DATABASE_URL=postgres://<YOUR_USER_NAME>:<YOUR_PASSWORD>@localhost:5432/analysocial
    export ADMINS='{"admins": [{"name": "<YOUR_NAME>", "email": "<YOUR_EMAIL>"}]}'

Set up db:

    createdb analysocial
    python manage.py migrate
    python manage.py createsuperuser  # Creates a superuser for the Admin, necessary to configure Facebook

Set up Facebook integration:

    Create a Facebook test application, with Facebook login (set Valid OAuth redirect URIs to localhost)
    python manage.py runserver
    Log into the Django admin
    Edit the Site to have the correct localhost url
    Create a Social application with info from Facebook (Client id == App ID, Secret key = App Secret, select site)

Run unit tests and view coverage:

    coverage run manage.py test
    coverage report -m
    
Speed up unit tests by setting environment variable:

    export REUSE_DB=1

Check code style:

    flake8 .
    
To generate a graph of the data models, you can use the following management command:

    python manage.py graph_models --pygraphviz -a -g -o all_models.png

Lint JavaScript:

    jshint */static/*/js

Run the development server:

    python manage.py runserver
    

Deployment
----------

This project is already set up for deployment to Heroku, on the app analysocial.

The Heroku apps have the following addons:
    
    heroku addons:create heroku-postgresql
    heroku addons:create sendgrid
    heroku addons:create newrelic
    heroku addons:create papertrail
    heroku addons:create scheduler
    
Set the Heroku config vars:

    ADMINS

Add Heroku buildpacks:

    heroku buildpacks:set heroku/nodejs -i 1
    heroku buildpacks:set heroku/python -i 2

To deploy directly to Heroku (right now, this is the only way to update static, etc.):

    sh scripts/deploy_to_heroku.sh
    
To push a specific branch to Heroku:

    git push -f heroku <local-branch>:refs/heads/master
    

TODO

* Add view of top 10 posts
* Analyze words in posts
* Sorting on posts view page
* CSV download from site
* Sync historical posts for new users (use RQ?)
* Email admin when new user signs up
