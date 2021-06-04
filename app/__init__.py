import logging
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import logging
#App Initializations
app=Flask(__name__)
app.config.from_object(config)

#Logging Setup
logging.basicConfig(level=logging.DEBUG)

#Login Setup
login=LoginManager(app)
login.login_view='login'
login.message='Please Login To Access The Page'
login.login_message_category='info'
#DB Setup
db=SQLAlchemy(app,session_options={"autoflush": False})
migrate=Migrate(app,db,render_as_batch=True)

from app import routes,models
from app.models import User,train,ticket,requests_,accepted_requests,denied_requests

#FLASK ADMIN SETTINGS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


#Admin Settings
app.config['FLASK_ADMIN_SWATCH']='cerulean'
admin=Admin(app,name='mer_app',template_mode='bootstrap3')
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(train,db.session))
admin.add_view(ModelView(ticket,db.session))
admin.add_view(ModelView(requests_,db.session))
admin.add_view(ModelView(accepted_requests,db.session))
admin.add_view(ModelView(denied_requests,db.session))
