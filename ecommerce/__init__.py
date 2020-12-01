import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import *
# from sqlalchemy import event
# from sqlalchemy.orm import backref
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from decouple import config
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import random
import string

app=Flask(__name__,template_folder='templates' ,static_folder='assets')

app.config['SECRET_KEY'] = 'hardsecretkey'
# userpass = 'mysql+pymysql://root:Aa555555@@'
# basedir  = '127.0.0.1'
# dbname   = '/fantasticecommerce'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{config("dbuser")}:{config("dbpass")}@{config("dbhost")}/{config("dbname")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db=SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True)
# migrate = Migrate(app, db,render_as_batch=True)
# manager=Manager(app)
# manager.add_command('db',MigrateCommand)
import ecommerce.admin.roots
import ecommerce.Auth.roots 