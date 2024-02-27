from flask import Flask, render_template, request, redirect, url_for, sessions
from .database import Base, engine, db_session, init_db, rebuild_db
from .models import Event, Participant, Role, Student, Organizer, Volunteer
from . import auth
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import json


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file("config.json", load=json.load)

    # rebuild when the app is run for the first time
    @app.before_first_request
    def before_first_request():
        rebuild_db()

    app.register_blueprint(auth.bp)

    admin = Admin(app, index_view=AdminIndexView(name='Home'))
    admin.add_view(ModelView(Event, db_session))
    admin.add_view(ModelView(Student, db_session))
    admin.add_view(ModelView(Participant, db_session))
    admin.add_view(ModelView(Organizer, db_session))
    admin.add_view(ModelView(Volunteer, db_session))
    admin.add_view(ModelView(Role, db_session))

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
