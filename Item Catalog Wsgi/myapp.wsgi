#!/usr/bin/python3.6
import sys
sys.path.insert(0,"/var/www/Flask_App/")
sys.path.insert(0,"/var/www/Flask_App/catalog/")
from catalog import app as application

application.secret_key = "secret_key"