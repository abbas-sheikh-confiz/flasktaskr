# project/_config.py

import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
CSRF_ENABLED = True
SECRET_KEY = '\r\xf5\xffO;Q\x07\x1a@\x91\xab\x9b*\x9c<\x15#\x86n\xc20\xf7\xe3-'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

# suppress command line warning
SQLALCHEMY_TRACK_MODIFICATIONS = True