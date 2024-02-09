from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from imessage_time_machine.config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.middleware.profiler import ProfilerMiddleware
import flask_profiler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config["DEBUG"] = True
app.config["flask_profiler"] = {
    "enabled": app.config["DEBUG"],
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth":{
        "enabled": True,
        "username": "admin",
        "password": "admin"
    },
    "ignore": [
	    "^/static/.*"
	]
}

login = LoginManager(app)
login.login_view = 'login'

from imessage_time_machine import routes, models, db_service
from imessage_time_machine.models import User, Message

flask_profiler.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    # db_service.init_login()
    db_service.init_messages(file="../mock_messages.txt")
    
    print(db.session.scalar(db.select(Message)))
    
    
