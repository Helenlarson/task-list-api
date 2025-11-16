from flask import Flask
from flask_migrate import Migrate          
from .db import db
from .models import task, goal
from .routes.task_routes import tasks_bp
from .routes.goal_routes import goals_bp
import os

def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate = Migrate(app, db)             

    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    return app

