# Flashcard

## About Flashcard

|         |                                                                |
| ------- | -------------------------------------------------------------- |
| Author  | Nnoduka Eruchalu                                               |
| Date    | 03/17/2019                                                     |
| Website | [http://flashcard.nnoduka.com/](http://flashcard.nnoduka.com/) |

[Flashcard](http://flashcard.nnoduka.com/) is quite the experience.


#### Available on Following Devices
* Modern web browsers


## Technologies
* Python
* PostgreSQL
* Amazon Web Services
* REST
* Javascript
* HTML
* CSS


## Software Description
| Module                       | Description                                   |
| ---------------------------- | --------------------------------------------- |
| `flashcard/settings.py`      | Django settings for project                   |
| `flashcard/settings_secret.py` | Secret Django settings for project          |
| `flashcard/template/`        | Utility functions to be used by templates     |
| `flashcard/urls.py`          | URL dispatcher for project                    |
| `flashcard/utils/`           | Utility functions useful to multiple apps     |
| `flashcard/views.py`         | View classes for endpoints not tied to apps   |
| `flashcard/wsgi.py`          | WSGI config for project                       |
|                              |                                               |
| **apps**                     | Django apps with backend logic                |
| `accounts/`                  | User account representation and auth. app     |
| `common/`                    | Custom fields, middleware, and utilities      |
| `cards/`                     | Words representationn app                     |
|                              |                                               |
| **`static/`**                | static files for project                      |
| `static/compass/`            | Compass project used to generate CSS file     |
| `static/css/`                | CSS files                                     |
| `static/img`                 | Static images                                 |
| `static/js/`                 | Javascript files                              |
|                              |                                               |
| **`templates/`**             | Django templates used by apps                 |
| `templates/403.html`         | 403 page                                      |
| `templates/404.html`         | 404 page                                      |
| `templates/500.html`         | 500 page                                      |
| `templates/base.html`        | base template used by all view templates      |
| `templates/email`            | base template used for emails                 |


### 3rd-party Python Modules
See [requirements.txt](requirements.txt)

### 3rd-party Javascript Modules
* [jQuery](http://jquery.com/)


### Design Decisions

#### REST API
##### General RESTful API Design Notes
Heroku has published a pretty good set of [design notes](https://github.com/interagent/http-api-design). 
This project tries to comply with these as much as possible.

##### Resource Identifiers
Publicly exposed identifiers (IDs), such as those exposed in RESTful URLs,
should not expose (or rely on) underlying technology. 

This [article](http://toddfredrich.com/ids-in-rest-api.html) gives a better
explanation of what to use as resource identifiers.


##### Model schema
All objects have `updated_at` datetimes to be used by client apps for sync
purposes. [[Ref](http://stackoverflow.com/a/5052208)]

## Virtual Env
Start a `virtualenv` virtual Python environment. This will create a sandbox
isolated from your existing Python installation so that installed packages
only exist within the sandbox:
```
python3 -m venv venv/
```

Activate the sandbox:
```
source venv/bin/activate
```

Install python libraries:
```
pip install -r requirements.txt
```

## Deployment
### Database (On local machine)
#### Create User
```
$ psql -U postgres
postgres=# create role <username> superuser nocreaterole createdb login PASSWORD '<password>';
postgres=# \q
```

#### Create database
Create the database with the following command:
```
$ createdb -O <username> -U <username> <dbname>
$ psql <dbname> -U <username>
<username>=# \q
```

You can now access the database with the following command:
```
$ psql <dbname> -U <username>
```

#### Drop database
Ideally this will only happen on a local machine
```
dropdb -U <username> <dbname>
```

### Django Setup: 
#### Settings files
The Django project is missing the `flashcard/settings_secret.py` file. A
template version is included for help in setting up the sensitive information
needed by the project.

#### Database Setup
Run the `python manage.py migrate` management command to create/update schema


### Server Setup Notes
These instructions here are what I did on my [Webfaction](https://www.webfaction.com/) server.

#### Virtual ENV notes
##### Create webfaction app with the following settings:
* Name: `flashcard`
* App category: `Django`
* App type: `Django 2.1.7 (mod_wsgi 4.6.5/Python 3.7)`
* The new application will be created in home directory (`~`) under `~/webapps/flashcard`.
* Delete the default project folder, `flashcard`
* git clone the project in its place

##### Create a virtual environment
* Turn application directory into a virtual Python environment:
  ```
  $ cd ~/webapps/flashcard
  $ python3.7 -m venv .
  ```

* This adds the folders and scripts for a virtual environment inside of the
  directory which webfaction created for our application.

* You can now activate the created environment:
  ```
  $ source bin/activate
  (flashcard) $ 
  ```

##### Install Django and other dependencies
* Once the initial Virtualenv setup is complete, you can install Django and
  other python packages inside it's `lib/python2.7/site-packages` directory
  ```
  (flashcard) $ pip install -r flashcard/requirements.txt
  ```

##### Ref
http://michal.karzynski.pl/blog/2013/09/14/django-in-virtualenv-on-webfactions-apache-with-mod-wsgi/

#### Crontab Additions
Access crontab with:
```
crontab -e
```

Edit it to perform following functionality:

* Setup PATH, PYTHONPATH to be used by cron's environment
* Restart apache every 20 minutes. This ensures minimal downtime (if at all)
* Backup database daily using configurations hidden in config file

```
PATH=/home/flashcard/webapps/flashcard/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/flashcard/bin:.

17,37,57 * * * * ~/webapps/flashcard/apache2/bin/start
```


## Miscellaneous

#### To Run Development Server
```
python manage.py runserver 0:8000
```
