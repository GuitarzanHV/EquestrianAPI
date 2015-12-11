EquinEval Web API and Administration
====================================

License TBD

This Web API and administration portal is meant to work with EquinEval mobile apps and the EquineEval website. This component is necessary to display and save EquinEval questionnaires.

Dependencies
------------
Python 3.4
Django 1.8
Django REST Framework 3.2.3
PyMySQL 1.3.6

Installation
------------

Make sure the root of the project is in a folder accessable to the webserver being used. /var/www/django makes a good enough spot. 

### Database setup
To unpack the MySQL database, make an `equestrian` database on your MySQL instance than from the project root folder run `mysql -u [username] -p [password] equestrian < EquinEval.sql`. 
In EquestrianAPI/production_settings.py, change the `'NAME'`, `'USER'`, and `'PASSWORD'` keys in the DATABASES dictionary to values that will allow access to the database.
Now run `python3 manage.py migrate --fake` to let Django know the database is prepared for its use.

### Webserver setup
In EquestrianAPI/wsgi.py, make sure the `sys.path.append()` command is the correct path to the project root.
In EquestrianAPI/production_settings.py, make sure `ALLOWED HOSTS` includes the hostname of your server.
Create a folder `django_static` under `/var/www/html`. Then run `python3 manage.py collectstatic` to populate the folder.
For Apache 2, paste this server configuration into the relevant .conf and modify as needed:

    Alias /static/ /var/www/html/django_static/

    <Directory /var/www/html/django_static>
    Require all granted
    </Directory>

    WSGIScriptAlias /API path/to/Equestrian_API/EquestrianAPI/wsgi.py
    WSGIPythonPath path/to/Equestrian_API

    <Directory path/to/Equestrian_API/EquestrianAPI>
    <Files wsgi.py>
    Allow from all
    </Files>
    </Directory>

Notes
-----

While production_settings.py is provided here for convenience, it should NOT be used for development or shared with the outside world. The information in it can lead to security breaches.
While not implemented currently, the SECRET_KEY should be set in production_settings.py for real-world deployment. For more information, visit the [Django Deployment Checklist](https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/)
