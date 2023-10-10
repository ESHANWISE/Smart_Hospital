from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate


csrf = CSRFProtect()

# function to creat db
def create_db():
     from pkg import app
     from pkg.models import db
     app.app_context().push()
     db.create_all()


def create_app():
     """keep all imports that may cause conflict within function so that anytime we write 
    "from pkg.. import.. none of these statements will be executed"""
     from pkg.models import db
     app = Flask(__name__)
     app.config.from_pyfile("config.py")
     db.init_app(app)
     migrate = Migrate(app,db)
     csrf.init_app(app)
     return (app)

app = create_app()

from pkg import userroute,adminroute,personnelroute
from pkg.forms import *
