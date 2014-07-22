#!/bin/bash
killall -9 python
~/bin/python manage.py runserver 0.0.0.0:8000
