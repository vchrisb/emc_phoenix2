#emc_phoenix2 [![Build Status](https://travis-ci.org/vchrisb/emc_phoenix2.svg?branch=master)](https://travis-ci.org/vchrisb/emc_phoenix2)

==========

## Conference App for the EMC Phoenix2 Event 2016 in Berlin

Leveraging:
* [Django](https://www.djangoproject.com/)
* Python
* [PostgreSQL](https://www.elephantsql.com/)
* [Bootstrap](http://getbootstrap.com/)
* Asynchronous tasks with [Celery](http://www.celeryproject.org/) and [RabbitMQ](http://www.rabbitmq.com/)
* S3 compatible ([EMC ECS](https://portal.ecstestdrive.com/)) storage backend
* Social Authentication
* REST Framework
* [Cloud Foundry](https://run.pivotal.io)
* Twitter Streams
* [New Relic](http://newrelic.com/)
* [Papertrail](https://papertrailapp.com/)
* [Sumologic](https://www.sumologic.com/)
* [Sendgrid](https://sendgrid.com)
* [Travis CI](https://travis-ci.org)
* [Slack](https://slack.com/)
* [Memcached](https://memcached.org/)

Overview:
![Overview](/static_custom/img/app_overview.png)

## Installation

Simplest way to test this app is to use ``Vagrant`` with ``vagrant up``. This will create a Fedora Virtualbox with all required packages and a python virtual environment.

## Configuration

### modify environments file for development
copy "environments.sh.example" environments.sh
modify environments.sh

### ECS

#### create ecs access keys
https://portal.ecstestdrive.com/

#### create buckets and corresponding CORS configuration (example below)
```
<CORSConfiguration>
 <CORSRule>
   <AllowedOrigin>http://www.example.com</AllowedOrigin>
   <AllowedMethod>PUT</AllowedMethod>
   <AllowedMethod>POST</AllowedMethod>
   <AllowedMethod>DELETE</AllowedMethod>
   <AllowedHeader>*</AllowedHeader>
 </CORSRule>
 <CORSRule>
   <AllowedOrigin>*</AllowedOrigin>
   <AllowedMethod>GET</AllowedMethod>
 </CORSRule>
</CORSConfiguration>
```

or more specific also for ```GET``` with ```http``` and ```https```

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <CORSRule>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>DELETE</AllowedMethod>
    <AllowedOrigin>http://www.example.com</AllowedOrigin>
    <AllowedHeader>*</AllowedHeader>
  </CORSRule>
  <CORSRule>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedOrigin>http://www.example.com</AllowedOrigin>
  </CORSRule>
  <CORSRule>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>DELETE</AllowedMethod>
    <AllowedOrigin>https//www.example.com</AllowedOrigin>
    <AllowedHeader>*</AllowedHeader>
  </CORSRule>
  <CORSRule>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedOrigin>https://www.example.com</AllowedOrigin>
  </CORSRule>
</CORSConfiguration>
```

to test CORS:
```
curl -i "http://static.1234567890.public.ecstestdrive.com/some/file.txt" -H "Origin: http://www.example.com"
```
and look for ```Access-Control-Allow-Origin: http://www.example.com``` in the response.


#### collectstatic at client
python manage.py collectstatic

### Logging

Create Account at https://papertrailapp.com and add three Services of type Cloud Foundry.  
More information at http://help.papertrailapp.com/kb/hosting-services/cloud-foundry/

### create social authentication

#### Google:
https://console.developers.google.com/

##### Create application
Create OAuth 2 Credentials -> Web application -> Authorized redirect URIs: http://app.domain.com/accounts/github/login/callback/

##### Enable API
Overview -> Google+ API -> Enable API

#### Twitter:
https://apps.twitter.com/

##### Create application
Create New App -> Callback URL: http://app.domain.com/accounts/twitter/login/callback/

#### Github:
https://github.com/settings/applications/new

##### Create application
Create New App -> Authorization callback URL: http://app.domain.com/accounts/github/login/callback/

#### Facebook:
https://developers.facebook.com/apps
Settings -> Advanced -> Valid OAuth redirect URIs: http://app.domain.com/accounts/facebook/login/callback/

#### cloud foundry

##### login to Cloud Foundry
```cf login -a https://api.run.pivotal.io```

##### create services
Example for Pivotal Web Service (run.pivotal.io)
```
cf create-service elephantsql turtle phoenix_db
cf create-service cloudamqp lemur phoenix_rabbitmq
cf create-service newrelic standard phoenix_newrelic
cf create-service sendgrid free sendgrid

cf cups phoenix_ecs -p '{"HOST":"object.ecstestdrive.com","ACCESS_KEY_ID":"123456789@ecstestdrive.emc.com","SECRET_ACCESS_KEY":"ABCDEFGHIJKLMNOPQRSTUVWXYZ","PUBLIC_URL":"123456789.public.ecstestdrive.com","STATIC_BUCKET":"static","MEDIA_BUCKET":"public","SECURE_BUCKET":"secure"}'
cf cups phoenix_twitter -p '{"CONSUMER_KEY":"ABCDEFGHIJKLMNOPQRSTUVWXYZ","CONSUMER_SECRET":"ABCDEFGHIJKLMNOPQRSTUVWXYZ","ACCESS_TOKEN":"ABCDEFGHIJKLMNOPQRSTUVWXYZ","ACCESS_TOKEN_SECRET":"ABCDEFGHIJKLMNOPQRSTUVWXYZ"}'
cf cups phoenix_config -p '{"SECRET_KEY":"ABCDEFGHIJKLMNOPQRSTUVWXYZ","DEBUG":"False","DEFAULT_FROM_EMAIL":"noreply@domain.local","DEFAULT_TO_EMAIL":"admin@domain.local","SERVER_EMAIL":"django@domain.local","ADMINS":"[('Admin', 'admin@domain.local')]"}'

cf cups phoenix_papertrail -l syslog://logs3.papertrailapp.com:12345
cf cups phoenix_celery_papertrail -l syslog://logs3.papertrailapp.com:12346
cf cups phoenix_watcher_papertrail -l syslog://logs3.papertrailapp.com:12347
```

if not using ```sendgrid```
```
cf cups phoenix_mail -p '{"HOST":"smtp.domain.local","USER":"django@domain.local","PASSWORD":"123456789","PORT":"25","TLS":"True"}'
```

##### initial push for database creation
Script will create a superuser ``admin`` with password ``admin``
```cf push phoenix --no-route -c "bash scripts/init_db.sh" -i 1```

##### migrate database
```cf push phoenix-migrate --no-route -c "bash scripts/migrate.sh" -i 1  
cf delete phoenix-migrate```

##### push app
```cf push phoenix```

For a non-disruptive push
```cf rename phoenix phoenix-old
cf push phoenix
cf delete phoenix-old --f```

##### push celery
```cf push phoenix-celery```

##### push twitter-watcher
```cf push phoenix-twitter-watcher```

#### Backup & Restore Database

##### Local Backup
```pg_dump postgres:///phoenix -F t > psqldump.tar```

##### Remote Backup
```pg_dump postgres://user:password@host.db.elephantsql.com:5432/database -F t > elephantsqldump.tar```

##### Local Restore
```
dropdb phoenix
sudo -u postgres createdb -U postgres --locale=en_US.utf-8 -E utf-8 -O vagrant phoenix -T template0
pg_restore -d phoenix psqldump.tar
```

#### Travis CI

This app is using [Travis CI](https://travis-ci.org) for continuous integration and continuous deployment to Cloud Foundry.
If your password includes symbols (such as braces, parentheses, backslashes, and pipe symbols), you must escape those symbols before running travis encrypt.
More Information regarding [Cloud Foundry Deployment](https://docs.travis-ci.com/user/deployment/cloudfoundry/).

```
travis encrypt --add deploy.username
travis encrypt --add deploy.password
```