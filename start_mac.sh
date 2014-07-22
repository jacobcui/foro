#!/bin/bash
killall -9 python

## python directory
# /opt/local/bin/python     -> /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# /opt/local/bin/pip        -> /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/pip
# /opt/local/bin/virtualenv -> /opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/virtualenv

/opt/local/lib/mysql5/bin/mysqladmin stop
/opt/local/lib/mysql5/bin/mysqld_safe&
../bin/python manage.py runserver 0.0.0.0:80

## Apache directory
#/opt/local/apache2/bin/apachectl restart
